import json
import logging
from functools import wraps

from quart import jsonify, request
from src.core.producer import get_producer

logger = logging.getLogger(__name__)


async def action(producer, data, schema, topic):
    try:
        # Валидируем данные через предоставленную схему
        validated_data = schema(**data)
        logger.debug(f"Validated data: {validated_data}")
        # Преобразуем данные в JSON
        message = json.dumps(validated_data.dict()).encode("utf-8")
        logger.debug(f"Encoded message: {message}")
        # Отправляем сообщение в Kafka
        await producer.send_and_wait(topic, message)
        logger.info(f"Message sent to topic {topic}: {message}")
        return {"status": "success"}
    except Exception as e:
        # Обработка исключений и логирование ошибок
        logger.error(f"Failed to send message to Kafka: {e}")
        return {"status": "error", "message": str(e)}


def common_endpoint(schema, topic):
    def decorator(func):
        @wraps(func)
        async def wrapper(*_, **__):
            data = await request.get_json()
            logger.info(f"Received data for {topic}: {data}")
            result = await common_handler(data, schema, topic)
            logger.info(f"Action result for {topic}: {result}")
            return jsonify(result)

        return wrapper

    return decorator


async def common_handler(data, schema, topic):
    producer = get_producer()
    result = await action(producer, data, schema, topic)
    return result
