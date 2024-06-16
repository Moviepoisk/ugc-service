from aiokafka import AIOKafkaProducer
from quart import Quart
from src.api import v1_router
from src.core.config import settings

producer: AIOKafkaProducer | None = None

app = Quart(__name__)
app.register_blueprint(v1_router)


@app.before_serving
async def start_producer():
    global producer
    producer = AIOKafkaProducer(bootstrap_servers=settings.kafka_bootstrap_servers, acks=settings.kafka_acks)
    await producer.start()


@app.after_serving
async def stop_producer():
    await producer.stop()


if __name__ == "__main__":
    app.run()
