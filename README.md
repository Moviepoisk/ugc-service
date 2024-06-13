# INFRA

docker compose up kafka-0 kafka-1 kafka-2 kafka-ui zookeeper clickhouse-node1 clickhouse-node2 clickhouse-node3 clickhouse-node4


# init kafka создание топиков
python -m create_topic user_clicks 3 2


# ugc-service в отдельном терминале
python -m app

# etl в отдельном терминале
python -m etl


# тест api запись сообщения 
curl -X POST http://localhost:5000/click -H "Content-Type: application/json" -d '{"user_id": "123", "timestamp": "2021-06-01T12:00:00"}'

# тест api запись сообщения можно через скрипт
python -m gen_test_msg
