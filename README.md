# Запуск
docker compose up 

# etl в отдельном терминале
cd /etl/src/
python -m etl

# тест api запись сообщения пример
curl -X POST http://localhost:5000/api/v1/click -H "Content-Type: application/json" -d '{"user_id": "87f5b737-19ab-4059-bc59-746bddb6b6b0", "timestamp": "2021-06-01T12:00:00"}'

# тест api запись сообщения можно через скрипт
cd /service/src/commands
python -m benchmark


# инициализация mongo_db кластера
chmod +x setup_mongo_cluster.sh
./setup_mongo_cluster.sh