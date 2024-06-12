
# init kafka создание топиков
python -m create_topic user_clicks 3 2


# ugc-service
python -m src/app


# тест api запись сообщения
curl -X POST http://localhost:5000/click -H "Content-Type: application/json" -d '{"user_id": "123", "timestamp": "2021-06-01T12:00:00"}'
