import logging
from app.models.classification import ClassificationResult
from app.services.classification_service import ClassificationService
from app.services.extraction_service import ExtractionService


class AggregationService:

    def __init__(self, repository):

        self.repository = repository

        self.classifier = ClassificationService()

        self.extractor = ExtractionService()

    def process_ocr(self, message):

        logging.info("\nПолучено сообщение doc.ocr.done")

        self.repository.mark_ocr_done(
            doc_id=message.doc_id,
            text=message.payload["text"]
        )

        logging.info("OCR сохранен в БД")

        return self.try_process(message.doc_id)

    def process_bert(self, message):

        logging.info("\nПолучено сообщение doc.bert.done")

        self.repository.mark_bert_done(
            doc_id=message.doc_id,
            doc_type=message.payload["doc_type"],
            confidence=message.payload["confidence"]
        )

        logging.info("BERT сохранен в БД")

        return self.try_process(message.doc_id)

    def process_yolo(self, message):

        logging.info("\nПолучено сообщение doc.yolo.done")

        self.repository.mark_yolo_done(
            doc_id=message.doc_id,
            doc_type=message.payload["doc_type"],
            confidence=message.payload["confidence"]
        )

        logging.info("YOLO сохранен в БД")

        return self.try_process(message.doc_id)

    def try_process(self, doc_id):

        if not self.repository.is_ready(doc_id):

            logging.info("Ожидаем остальные сообщения...")

            return None

        logging.info("\nВсе сообщения получены.")

        state = self.repository.load_document(doc_id)

        bert_result = ClassificationResult(
            model="bert",
            doc_type=state.bert_type,
            confidence=state.bert_confidence
        )

        yolo_result = ClassificationResult(
            model="yolo",
            doc_type=state.yolo_type,
            confidence=state.yolo_confidence
        )

        final = self.classifier.resolve_document_type(
            bert_result,
            yolo_result
        )

        self.repository.save_document_type(
            doc_id,
            final.doc_type
        )

        logging.info(f"Итоговый тип: {final.doc_type}")

        fields = self.extractor.extract(
            state.ocr_text,
            final.doc_type
        )

        self.repository.save_extracted_fields(
            doc_id=doc_id,
            doc_type=final.doc_type,
            confidence=final.confidence,
            fields=fields
        )

        return {
            "classification": final,
            "fields": fields
        }