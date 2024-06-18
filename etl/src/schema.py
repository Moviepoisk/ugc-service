def create_table_sql(topic_name):
    return f"""
    CREATE TABLE IF NOT EXISTS {topic_name} (
        user_id UUID,
        timestamp DateTime64(3, 'UTC'),  # DateTime64 с поддержкой миллисекунд и UTC временной зоны
        data String
    ) ENGINE = MergeTree()
    ORDER BY (timestamp);
    """


def insert_into_table_sql(topic_name):
    return f"INSERT INTO {topic_name} (user_id, timestamp, data) VALUES"
