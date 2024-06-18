import asyncio
import json
from datetime import datetime, timezone

from aiokafka import AIOKafkaConsumer, TopicPartition
from asynch import connect
from schema import SQL_CREATE_TABLE_CLICK, SQL_INSERT_INTO_TABLE_CLICK


async def create_clickhouse_client():
    client = await connect("clickhouse://default:@localhost/default")
    async with client.cursor() as cursor:
        await cursor.execute(SQL_CREATE_TABLE_CLICK)
    return client


async def consume_messages(consumer, buffer, messages):
    async for msg in consumer:
        if msg.value is not None:
            message_value = msg.value.decode("utf-8")
            if message_value.strip():  # Проверяем, что сообщение не пустое
                try:
                    data = json.loads(message_value)
                    buffer.append((data["user_id"], data["timestamp"]))
                    messages.append(
                        msg
                    )  # Добавляем сообщение в список для последующего подтверждения
                    print(f"Buffered message: {data}")
                except json.JSONDecodeError as e:
                    print(
                        f"Ошибка декодирования JSON: {e} - Содержимое: {message_value}"
                    )
                    continue


async def insert_data_periodically(cursor, buffer, consumer, messages):
    while True:
        await asyncio.sleep(10)
        current_time = datetime.now(timezone.utc)
        print(f"Buffer length: {len(buffer)}")

        if buffer:
            print(f"Inserting {len(buffer)} messages into ClickHouse.")
            await cursor.execute(SQL_INSERT_INTO_TABLE_CLICK, buffer)
            buffer.clear()
            print(f"Data inserted at {current_time}")

            # Подтверждение смещений после успешной вставки данных
            offsets = {
                TopicPartition(msg.topic, msg.partition): msg.offset + 1
                for msg in messages
            }
            await consumer.commit(offsets)
            messages.clear()
            print("Offsets committed.")


async def consume_and_insert():
    consumer = AIOKafkaConsumer(
        "user_clicks",
        bootstrap_servers="localhost:9094",
        group_id="clickhouse_group",
        enable_auto_commit=False,  # Отключаем автоматическое подтверждение
    )
    await consumer.start()
    print("Kafka consumer started.")
    clickhouse_client = await create_clickhouse_client()
    print("Connected to ClickHouse.")
    buffer = []
    messages = []

    async with clickhouse_client.cursor() as cursor:
        consumer_task = asyncio.create_task(
            consume_messages(consumer, buffer, messages)
        )
        insert_task = asyncio.create_task(
            insert_data_periodically(cursor, buffer, consumer, messages)
        )

        await asyncio.gather(consumer_task, insert_task)

    await consumer.stop()
    print("Kafka consumer stopped.")


async def main():
    await consume_and_insert()


if __name__ == "__main__":
    asyncio.run(main())
