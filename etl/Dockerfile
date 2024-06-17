FROM python:3.11-slim-bookworm as builder

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

COPY ./src ./src

RUN chmod +x ./entrypoint.sh

EXPOSE 8000

USER app

ENTRYPOINT ["./entrypoint.sh"]
