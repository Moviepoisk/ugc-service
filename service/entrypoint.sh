#!/bin/bash

set -e


python commands/create_topics.py \
  --bootstrap-servers kafka-0:9092,kafka-1:9092,kafka-2:9092 \
  --num-partitions 3 \
  --replication-factor 2

if [[ "$DEBUG" = "True" ]]
then
  uvicorn src.main:app --host "$HOST" --port "$PORT" --reload --workers "$WORKERS" --log-level "$LOG_LEVEL"
else
  gunicorn src.main:app --bind  "$HOST:$PORT" --workers "$WORKERS" --log-level "$LOG_LEVEL" -k uvicorn.workers.UvicornWorker
fi
