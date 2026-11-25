import json
import logging

from aiokafka import AIOKafkaConsumer

from app.config import settings
from app.kafka.dispatcher import KafkaDispatcher
from app.schemas.kafka_messages import KafkaMessage

logger = logging.getLogger(__name__)


class KafkaConsumerService:

    def __init__(self):

        self.dispatcher = KafkaDispatcher()

        self.consumer = AIOKafkaConsumer(
            "doc.ocr.done",
            "doc.bert.done",
            "doc.yolo.done",
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            group_id="ms5"
        )

    async def start(self):

        await self.consumer.start()

        logger.info("Kafka Consumer started.")

        try:

            async for message in self.consumer:

                payload = json.loads(
                    message.value.decode()
                )

                kafka_message = KafkaMessage(
                    doc_id=payload["doc_id"],
                    trace_id=payload.get("trace_id", ""),
                    service=payload.get("service", ""),
                    payload=payload["payload"]
                )

                self.dispatcher.dispatch(
                    message.topic,
                    kafka_message
                )

        finally:

            await self.consumer.stop()

            logger.info("Kafka Consumer stopped.")