import argparse
import logging

from confluent_kafka.admin import AdminClient, KafkaException, NewTopic
from src.schemas.base import KafkaTopic

logger = logging.getLogger(__name__)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Create Kafka topics with specified parameters."
    )
    parser.add_argument(
        "--bootstrap-servers", type=str, required=True, help="Kafka bootstrap servers"
    )
    parser.add_argument(
        "--num-partitions",
        type=int,
        required=True,
        help="Number of partitions for the topics",
    )
    parser.add_argument(
        "--replication-factor",
        type=int,
        required=True,
        help="Replication factor for the topics",
    )
    return parser.parse_args()


def main(args):
    """Создает Kafka топик с заданными параметрами."""
    admin_client = AdminClient({"bootstrap.servers": args.bootstrap_servers})
    topics = [
        NewTopic(
            topic=topic.value,  # Получаем строковое значение топика через .value
            num_partitions=args.num_partitions,
            replication_factor=args.replication_factor,
        )
        for topic in KafkaTopic  # Итерация по элементам Enum
    ]

    try:
        result = admin_client.create_topics(new_topics=topics)
        for topic, f in result.items():
            try:
                f.result()
                logger.info(f"Topic '{topic}' created successfully.")
            except Exception as e:
                logger.error(f"Failed to create topic {topic}: {e}")
    except KafkaException as ke:
        logger.error(f"Failed to connect to Kafka broker: {ke}")


if __name__ == "__main__":
    args = parse_arguments()
    main(args=args)
