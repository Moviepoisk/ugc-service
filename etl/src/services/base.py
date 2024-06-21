import logging

from aiokafka import AIOKafkaConsumer
from clickhouse_driver import Client as ClickhouseClient

logger = logging.getLogger(__name__)


class ClickhouseConnectionManager:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.client = None
        logger.debug(f"Initialized ClickhouseConnectionManager")

    async def connect(self):
        try:
            self.client = ClickhouseClient.from_url(self.connection_string)
            logger.info("Connected to Clickhouse")
        except Exception as e:
            logger.error(f"Failed to connect to Clickhouse: {e}")
            raise

    async def execute_query(self, query):
        try:
            async with self.client.cursor() as cursor:
                await cursor.execute(query)
                logger.info(f"Executed query: {query}")
        except Exception as e:
            logger.error(f"Failed to execute query: {query}, Error: {e}")
            raise


class KafkaConsumerManager:
    def __init__(self, topics, bootstrap_servers, group_id):
        self.topics = topics
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self.consumer = None
        logger.debug(
            f"Initialized KafkaConsumerManager with topics: {topics}, bootstrap_servers: {bootstrap_servers}, group_id: {group_id}"
        )

    async def start(self):
        try:
            self.consumer = AIOKafkaConsumer(
                *self.topics, bootstrap_servers=self.bootstrap_servers, group_id=self.group_id, enable_auto_commit=False
            )
            await self.consumer.start()
            logger.info("Kafka consumer started")
        except Exception as e:
            logger.error(f"Failed to start Kafka consumer: {e}")
            raise

    async def stop(self):
        if self.consumer:
            try:
                await self.consumer.stop()
                logger.info("Kafka consumer stopped")
            except Exception as e:
                logger.error(f"Failed to stop Kafka consumer: {e}")
                raise

    async def consume_messages(self):
        try:
            async for msg in self.consumer:
                logger.debug(f"Consumed message: {msg}")
                yield msg
        except Exception as e:
            logger.error(f"Error consuming messages: {e}")
            raise

    async def commit_offsets(self, offsets):
        try:
            await self.consumer.commit(offsets)
            logger.info(f"Committed offsets: {offsets}")
        except Exception as e:
            logger.error(f"Failed to commit offsets: {offsets}, Error: {e}")
            raise
