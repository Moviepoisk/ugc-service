from confluent_kafka.admin import AdminClient, NewTopic, KafkaException
import sys

def create_kafka_topic(topic_name, partitions, replication_factor, brokers="127.0.0.1:9094"):
    """
    Создает Kafka топик с заданными параметрами.

    :param topic_name: имя топика
    :param partitions: количество партиций
    :param replication_factor: фактор репликации
    :param brokers: адрес Kafka брокера
    """
    # Создаем административный клиент Kafka
    admin_client = AdminClient({
        "bootstrap.servers": brokers
    })

    # Создаем новый топик
    topic = NewTopic(topic_name, num_partitions=partitions, replication_factor=replication_factor)

    # Отправляем запрос на создание топика
    try:
        result = admin_client.create_topics([topic])
        for topic, f in result.items():
            try:
                f.result()  # Блокирующий вызов
                print(f"Topic '{topic}' created successfully.")
            except Exception as e:
                print(f"Failed to create topic {topic}: {e}")
    except KafkaException as ke:
        print(f"Failed to connect to Kafka broker: {ke}")

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python create_topic.py <topic_name> <partitions> <replication_factor>")
        sys.exit(1)

    topic_name = sys.argv[1]
    partitions = int(sys.argv[2])
    replication_factor = int(sys.argv[3])

    create_kafka_topic(topic_name, partitions, replication_factor)