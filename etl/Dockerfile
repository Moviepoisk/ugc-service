FROM python:3.11-slim-bookworm as builder
ENV PYTHONUNBUFFERED=1 PYTHONPATH="$PYTHONPATH:/opt:/opt/src"

WORKDIR /opt

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt ./requirements.txt

RUN apt-get update  \
    && apt-get install -y gcc  \
    && apt install netcat-traditional  \
    && pip install --upgrade pip  \
    && pip install -r ./requirements.txt --no-cache-dir

FROM builder

RUN groupadd -r app  \
    && useradd -d /opt -r -g app app \
    && mkdir -p /opt/logs \
    && chown app:app -R /opt/

COPY . .

RUN chmod +x ./entrypoint.sh

USER app

ENTRYPOINT ["./entrypoint.sh"]
