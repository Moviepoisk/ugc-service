from http import HTTPStatus

from pydantic import BaseModel, ValidationError
from quart import jsonify
from src.main import producer


async def action(data: dict, schema: type[BaseModel], topic: str):
    try:
        event = schema(user_id=data.get("user_id"), timestamp=data.get("timestamp"))
    except ValidationError as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST

    message = event.json()  # Автоматическое формирование JSON-строки из модели

    try:
        await producer.send_and_wait(topic=topic, value=message.encode("utf-8"))
        return jsonify({"status": "Message sent successfully"}), HTTPStatus.OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
