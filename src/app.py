import asyncio
from quart import Quart, request, jsonify
from aiokafka import AIOKafkaProducer
from pydantic import ValidationError

from schema import ClickData

app = Quart(__name__)


producer = None

@app.before_serving
async def start_producer():
    global producer
    # Исправленная конфигурация Kafka Producer
    producer_config = {
        'bootstrap_servers': '127.0.0.1:9094',  # Исправлено с 'bootstrap.servers' на 'bootstrap_servers'
        'acks': 'all'  # Настройка свойства acks
    }
    producer = AIOKafkaProducer(**producer_config)
    await producer.start()

@app.after_serving
async def stop_producer():
    await producer.stop()

@app.route('/click', methods=['POST'])
async def click():
    try:
        data = await request.get_json()
        event = ClickData(**data)
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400

    message = event.json()  # Автоматическое формирование JSON-строки из модели

    try:
        await producer.send_and_wait('user_clicks', message.encode('utf-8'))
        return jsonify({'status': 'Message sent successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')