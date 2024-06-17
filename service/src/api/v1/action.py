import json


async def action(producer, data, schema, topic):
    try:
        # Валидируем данные через предоставленную схему
        validated_data = schema(**data)
        # Преобразуем данные в JSON
        message = json.dumps(validated_data.dict()).encode("utf-8")
        # Отправляем сообщение в Kafka
        await producer.send_and_wait(topic, message)
        return {"status": "success"}
    except Exception as e:
        # Обработка исключений и логирование ошибок
        print(f"Failed to send message to Kafka: {e}")
        return {"status": "error", "message": str(e)}
