import json
import logging
import re
from datetime import datetime, timezone

from aiokafka import ConsumerRecord, TopicPartition
from src.schemas.base import insert_into_table_sql
from src.services.base import ClickhouseConnectionManager, KafkaConsumerManager

logger = logging.getLogger(__name__)


class KafkaClickhouseETL:
    def __init__(
        self,
        consumer_manager: KafkaConsumerManager,
        clickhouse_manager: ClickhouseConnectionManager,
        flush_interval: int = 5,
        max_buffer_size: int = 10000,
    ) -> None:
        self.consumer_manager = consumer_manager
        self.clickhouse_manager = clickhouse_manager
        self.flush_interval = flush_interval
        self.max_buffer_size = max_buffer_size
        self.buffer: dict[str, list] = {topic: [] for topic in self.consumer_manager.topics}
        self.messages: dict[str, list[ConsumerRecord]] = {topic: [] for topic in self.consumer_manager.topics}
        self.last_flush_time = datetime.now(timezone.utc)
        logger.debug(
            f"Initialized KafkaClickhouseETL with flush_interval: {flush_interval}, max_buffer_size: {max_buffer_size}"
        )

    async def check_and_flush_data(self) -> None:
        current_time = datetime.now(timezone.utc)
        if (current_time - self.last_flush_time).total_seconds() > self.flush_interval or any(
            len(buf) >= self.max_buffer_size for buf in self.buffer.values()
        ):
            await self.flush_data()

    async def flush_data(self) -> None:
        for topic, data in self.buffer.items():
            if data:
                for record in data:
                    query = insert_into_table_sql(topic, record)
                    try:
                        await self.clickhouse_manager.execute_query(query)
                    except Exception as e:
                        logger.error(f"Error executing query for topic {topic}: {e}")

                logger.info(f"Flushed {len(self.buffer[topic])} records for topic {topic}.")
                self.buffer[topic].clear()
        self.last_flush_time = datetime.now(timezone.utc)
        await self.commit_offsets()

    async def commit_offsets(self) -> None:
        offsets = {
            TopicPartition(msg.topic, msg.partition): msg.offset + 1
            for topic_msgs in self.messages.values()
            for msg in topic_msgs
        }
        await self.consumer_manager.commit_offsets(offsets)
        for msgs in self.messages.values():
            msgs.clear()
        logger.info(f"Committed offsets and cleared message buffers")

    async def process_message(self, msg: ConsumerRecord) -> None:
        topic = msg.topic
        message_value = self.decode_message(msg)
        if not message_value:
            logger.warning(f"Failed to decode message: {msg}")
            return

        data = self.parse_message(message_value)
        if not data:
            logger.warning(f"Failed to parse message: {message_value}")
            return

        if not self.validate_and_format_timestamp(data):
            logger.warning(f"Failed to validate or format timestamp for message: {data}")
            return

        self.buffer[topic].append({"user_id": data["user_id"], "timestamp": data["timestamp"]})
        self.messages[topic].append(msg)
        await self.check_and_flush_data()
        logger.debug(f"Processed message for topic {topic}")

    @staticmethod
    def decode_message(msg: ConsumerRecord) -> str | None:
        try:
            return msg.value.decode("utf-8")
        except AttributeError:
            return None

    @staticmethod
    def parse_message(message_value: str) -> dict[str] | None:
        try:
            return json.loads(message_value)
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {e} - Content: {message_value}")
            return None

    @staticmethod
    def validate_and_format_timestamp(data: dict[str] | None) -> bool:
        timestamp = data.get("timestamp")
        if timestamp and KafkaClickhouseETL.is_valid_iso_format(timestamp):
            dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            data["timestamp"] = dt.strftime("%Y-%m-%d %H:%M:%S")
            return True
        else:
            logger.error(f"Invalid or missing timestamp: {timestamp}")
            return False

    @staticmethod
    def is_valid_iso_format(timestamp: str) -> bool:
        iso_format = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})$")
        return bool(iso_format.match(timestamp))

    async def run(self) -> None:
        await self.clickhouse_manager.connect()
        await self.consumer_manager.start()
        try:
            async for msg in self.consumer_manager.consume_messages():
                await self.process_message(msg)
        finally:
            await self.consumer_manager.stop()
            logger.info("ETL run completed")
