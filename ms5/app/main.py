from contextlib import asynccontextmanager
import asyncio
import logging

from fastapi import FastAPI

from app.config import settings
from app.kafka.consumer import KafkaConsumerService


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)

logger = logging.getLogger(__name__)

consumer = KafkaConsumerService()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Запускается при старте и остановке приложения.
    """

    logger.info("Starting MS5 service...")

    consumer_task = asyncio.create_task(
        consumer.start()
    )

    logger.info("Kafka Consumer started.")

    yield

    logger.info("Stopping MS5 service...")

    consumer_task.cancel()

    logger.info("MS5 stopped.")


app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan
)


@app.get("/")
def health():

    return {
        "service": settings.APP_NAME,
        "status": "running"
    }


@app.get("/health")
def health_check():

    return {
        "status": "ok"
    }