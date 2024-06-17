from aiokafka import AIOKafkaProducer
from src.core.config import settings

producer: AIOKafkaProducer | None = None


async def start_producer():
    global producer
    producer = AIOKafkaProducer(
        bootstrap_servers=settings.kafka_bootstrap_servers, acks=settings.kafka_acks
    )
    await producer.start()


async def stop_producer():
    await producer.stop()


def get_producer() -> AIOKafkaProducer:
    global producer
    return producer
