import asyncio

from src.core.config import settings
from src.schemas.base import KafkaTopic
from src.services.kafka_clickhouse import (
    ClickhouseConnectionManager,
    KafkaClickhouseETL,
    KafkaConsumerManager,
)

if __name__ == "__main__":
    kafka_consumer_manager = KafkaConsumerManager(
        topics=[topic.value for topic in KafkaTopic],
        bootstrap_servers=settings.kafka_host,
        group_id=settings.clickhouse_group,
    )
    clickhouse_manager = ClickhouseConnectionManager(settings.clickhouse_connection_url)
    etl = KafkaClickhouseETL(consumer_manager=kafka_consumer_manager, clickhouse_manager=clickhouse_manager)
    asyncio.run(etl.run())
