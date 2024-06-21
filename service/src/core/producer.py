import logging

from aiokafka import AIOKafkaProducer
from src.core.config import settings

logger = logging.getLogger(__name__)

producer: AIOKafkaProducer | None = None


async def start_producer():
    global producer
    try:
        producer = AIOKafkaProducer(bootstrap_servers=settings.kafka_host, acks=settings.kafka_acks)
        await producer.start()
        logger.info("Kafka producer started successfully.")
    except Exception as e:
        logger.error(f"Failed to start Kafka producer: {e}")
        raise


async def stop_producer():
    global producer
    if producer:
        try:
            await producer.stop()
            logger.info("Kafka producer stopped successfully.")
        except Exception as e:
            logger.error(f"Failed to stop Kafka producer: {e}")
            raise
    else:
        logger.warning("Attempted to stop Kafka producer, but it was not running.")


def get_producer() -> AIOKafkaProducer:
    global producer
    if not producer:
        logger.warning("Kafka producer is not initialized.")
    return producer
