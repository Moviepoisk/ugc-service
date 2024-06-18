import asyncio
import json
from datetime import datetime, timezone
from aiokafka import AIOKafkaConsumer, TopicPartition
from asynch import connect
from base import create_table_sql, insert_into_table_sql
from base import KafkaTopic
from dateutil import parser

class KafkaClickhouseETL:
    def __init__(
        self,
        bootstrap_servers,
        group_id,
        flush_interval=5,
        max_buffer_size=10000,
    ):
        self.topics = [topic.value for topic in KafkaTopic]
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self.flush_interval = flush_interval
        self.max_buffer_size = max_buffer_size
        self.buffer = {topic: [] for topic in self.topics}
        self.messages = {topic: [] for topic in self.topics}
        self.last_flush_time = datetime.now(timezone.utc)
        self.consumer = None
        self.clickhouse_client = None

    async def connect_to_clickhouse(self):
        self.clickhouse_client = await connect("clickhouse://default:@localhost/default")
        async with self.clickhouse_client.cursor() as cursor:
            for topic in self.topics:
                await cursor.execute(create_table_sql(topic))

    async def start_consumer(self):
        self.consumer = AIOKafkaConsumer(
            *self.topics,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            enable_auto_commit=False,
        )
        await self.consumer.start()
        print("Kafka consumer started.")

    async def consume_messages(self):
        async for msg in self.consumer:
            topic = msg.topic
            if msg.value is not None:
                message_value = msg.value.decode("utf-8")
                if message_value.strip():
                    try:
                        data = json.loads(message_value)
                        if "timestamp" in data:
                            dt = parser.isoparse(data["timestamp"])
                            data["timestamp"] = dt.strftime("%Y-%m-%d %H:%M:%S")
                        self.buffer[topic].append(
                            {"user_id": data["user_id"], "timestamp": data["timestamp"]}
                        )
                        await self.maybe_flush_data()
                        self.messages[topic].append(msg)
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON: {e} - Content: {message_value}")

    async def maybe_flush_data(self):
        current_time = datetime.now(timezone.utc)
        if (current_time - self.last_flush_time).total_seconds() > self.flush_interval or any(
            len(buf) >= self.max_buffer_size for buf in self.buffer.values()
        ):
            await self.flush_data()

    async def flush_data(self):
        async with self.clickhouse_client.cursor() as cursor:
            for topic, data in self.buffer.items():
                if data:
                    for record in data:
                        query = insert_into_table_sql(topic, record)
                        await cursor.execute(query)
                    print(f"Flushed {len(self.buffer[topic])} records for topic {topic}.")
                    self.buffer[topic].clear()
            self.last_flush_time = datetime.now(timezone.utc)
            await self.commit_offsets()

    async def commit_offsets(self):
        offsets = {
            TopicPartition(msg.topic, msg.partition): msg.offset + 1
            for topic_msgs in self.messages.values()
            for msg in topic_msgs
        }
        await self.consumer.commit(offsets)
        for msgs in self.messages.values():
            msgs.clear()

    async def run(self):
        await self.connect_to_clickhouse()
        await self.start_consumer()
        try:
            await self.consume_messages()
        finally:
            await self.consumer.stop()

if __name__ == "__main__":
    etl = KafkaClickhouseETL(
        bootstrap_servers="localhost:9094",
        group_id="clickhouse_group"
    )
    asyncio.run(etl.run())
