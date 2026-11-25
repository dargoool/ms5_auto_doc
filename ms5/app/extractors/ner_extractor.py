from natasha import (
    Segmenter,
    NewsEmbedding,
    NewsNERTagger,
    Doc,
)

from .patterns import PATTERNS


class NERExtractor:

    def __init__(self):

        self.segmenter = Segmenter()

        emb = NewsEmbedding()

        self.ner_tagger = NewsNERTagger(emb)
    
    def clean_entity(self, field: str, text: str) -> str:
        """
        Очищает значение, извлеченное NER.
        """

        # Убираем лишние переносы строк и двойные пробелы
        text = " ".join(text.split())

        # Для ФИО оставляем только первые три слова
        if field == "fio":
            return " ".join(text.split()[:3])

        return text

    def extract(self, text: str, doc_type: str):

        document = PATTERNS.get(doc_type)

        if not document:
            return {}

        result = {}

        # Создаем все поля заранее
        ner_fields = document.get("ner", {})

        for field in ner_fields:
            result[field] = {
                "value": None,
                "method": "ner"
            }

        # Если текст пустой — сразу возвращаем структуру
        if not text.strip():
            return result

        doc = Doc(text)

        doc.segment(self.segmenter)

        doc.tag_ner(self.ner_tagger)

        # Заполняем найденные значения
        for span in doc.spans:

            for field, entity_type in ner_fields.items():

                if span.type == entity_type:

                    value = self.clean_entity(field, span.text)

                    result[field] = {
                        "value": value,
                        "method": "ner"
                    }

        return result