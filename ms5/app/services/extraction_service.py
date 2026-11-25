from app.extractors.regex_extractor import RegexExtractor
from app.extractors.ner_extractor import NERExtractor
from app.services.classification_service import ClassificationService


class ExtractionService:

    def __init__(self):

        self.regex = RegexExtractor()

        self.ner = NERExtractor()

        self.classifier = ClassificationService()

    def extract(self, text: str, doc_type: str):

        regex_result = self.regex.extract(text, doc_type)

        ner_result = self.ner.extract(text, doc_type)

        result = {}

        result.update(regex_result)

        result.update(ner_result)

        return result
    
    def process(
        self,
        text: str,
        bert_result,
        yolo_result
    ):
        """
        Полный цикл обработки документа.
        """

        classification = self.classifier.resolve_document_type(
            bert_result,
            yolo_result
        )

        return self.extract(
            text,
            classification.doc_type
        )