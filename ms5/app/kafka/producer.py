import json
import logging

from aiokafka import AIOKafkaProducer

from app.config import settings

logger = logging.getLogger(__name__)


class KafkaProducerService:

    def __init__(self):

        self.producer = AIOKafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS
        )

    async def start(self):

        await self.producer.start()
        logger.info("Kafka Producer started.")

    async def stop(self):

        await self.producer.stop()
        logger.info("Kafka Producer stopped.")

    async def send(self, topic: str, message: dict):

        await self.producer.send_and_wait(
            topic,
            json.dumps(message).encode("utf-8")
        )

        logger.info(f"Message sent to '{topic}'.")