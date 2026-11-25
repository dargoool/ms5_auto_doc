from app.db.database import SessionLocal
from app.db.repository import Repository
from app.services.aggregation_service import AggregationService


class KafkaDispatcher:

    def dispatch(self, topic: str, message):

        db = SessionLocal()

        try:

            repository = Repository(db)

            aggregator = AggregationService(repository)

            if topic == "doc.ocr.done":
                return aggregator.process_ocr(message)

            elif topic == "doc.bert.done":
                return aggregator.process_bert(message)

            elif topic == "doc.yolo.done":
                return aggregator.process_yolo(message)

            raise ValueError(f"Unknown topic: {topic}")

        finally:
            db.close()