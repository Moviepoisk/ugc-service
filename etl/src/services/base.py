from aiokafka import AIOKafkaConsumer
from clickhouse_driver import Client as ClickhouseClient


class ClickhouseConnectionManager:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.client = None

    async def connect(self):
        self.client = ClickhouseClient.from_url(self.connection_string)

    async def execute_query(self, query):
        async with self.client.cursor() as cursor:
            await cursor.execute(query)


class KafkaConsumerManager:
    def __init__(self, topics, bootstrap_servers, group_id):
        self.topics = topics
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self.consumer = None

    async def start(self):
        self.consumer = AIOKafkaConsumer(
            *self.topics, bootstrap_servers=self.bootstrap_servers, group_id=self.group_id, enable_auto_commit=False
        )
        await self.consumer.start()

    async def stop(self):
        if self.consumer:
            await self.consumer.stop()

    async def consume_messages(self):
        async for msg in self.consumer:
            yield msg

    async def commit_offsets(self, offsets):
        await self.consumer.commit(offsets)
