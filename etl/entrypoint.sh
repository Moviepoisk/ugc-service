#!/bin/bash

while ! nc -z "$KAFKA_HOST" "$KAFKA_PORT"; do
      echo "Waiting $KAFKA_HOST"
      sleep 1.0
done

python src/main.py