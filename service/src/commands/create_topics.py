import argparse

from confluent_kafka.admin import AdminClient, KafkaException, NewTopic
from src.core.config.base import KafkaTopic


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
            topic=topic,
            num_partitions=args.num_partitions,
            replication_factor=args.replication_factor,
        )
        for topic in KafkaTopic
    ]

    try:
        result = admin_client.create_topics(new_topics=topics)
        for topic, f in result.items():
            try:
                f.result()
                print(f"Topic '{topic}' created successfully.")
            except Exception as e:
                print(f"Failed to create topic {topic}: {e}")
    except KafkaException as ke:
        print(f"Failed to connect to Kafka broker: {ke}")


if __name__ == "__main__":
    args = parse_arguments()
    main(args=args)
