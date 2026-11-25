from sqlalchemy.orm import Session

from app.db.models import DocumentState, ExtractedFields


class Repository:

    def __init__(self, db: Session):
        self.db = db

    # -------------------------------------------------
    # Работа с состоянием документа
    # -------------------------------------------------

    def get_or_create_state(self, doc_id: str) -> DocumentState:

        state = (
            self.db.query(DocumentState)
            .filter(DocumentState.doc_id == doc_id)
            .first()
        )

        if state is None:

            state = DocumentState(doc_id=doc_id)

            self.db.add(state)

            self.db.commit()

            self.db.refresh(state)

        return state

    def mark_ocr_done(
        self,
        doc_id: str,
        text: str
    ):

        state = self.get_or_create_state(doc_id)

        state.ocr_done = True
        state.ocr_text = text

        self.db.commit()

    def mark_bert_done(
        self,
        doc_id: str,
        doc_type: str,
        confidence: float
    ):

        state = self.get_or_create_state(doc_id)

        state.bert_done = True
        state.bert_type = doc_type
        state.bert_confidence = confidence

        self.db.commit()

    def mark_yolo_done(
        self,
        doc_id: str,
        doc_type: str,
        confidence: float
    ):

        state = self.get_or_create_state(doc_id)

        state.yolo_done = True
        state.yolo_type = doc_type
        state.yolo_confidence = confidence

        self.db.commit()

    # -------------------------------------------------
    # Проверка готовности
    # -------------------------------------------------

    def is_ready(self, doc_id: str) -> bool:

        state = self.get_or_create_state(doc_id)

        return (
            state.ocr_done
            and state.bert_done
            and state.yolo_done
        )

    # -------------------------------------------------
    # Получение данных документа
    # -------------------------------------------------

    def load_document(
        self,
        doc_id: str
    ) -> DocumentState:

        return self.get_or_create_state(doc_id)

    # -------------------------------------------------
    # Итоговый тип документа
    # -------------------------------------------------

    def save_document_type(
        self,
        doc_id: str,
        doc_type: str
    ):

        state = self.get_or_create_state(doc_id)

        state.doc_type = doc_type

        self.db.commit()

    # -------------------------------------------------
    # Сохранение результата извлечения
    # -------------------------------------------------

    def save_extracted_fields(
        self,
        doc_id: str,
        doc_type: str,
        confidence: float,
        fields: dict
    ):

        extracted = ExtractedFields(
            doc_id=doc_id,
            doc_type=doc_type,
            classification_confidence=confidence,
            fields=fields
        )

        self.db.add(extracted)

        self.db.commit()