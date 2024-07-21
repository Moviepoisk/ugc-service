FROM python:3.11-slim-bookworm as builder

WORKDIR /app

COPY ./infra/app/requirements.txt ./infra/requirements.txt

RUN apt-get update  \
    && pip install --upgrade pip  \
    && pip install -r ./infra/requirements.txt --no-cache-dir


FROM builder

COPY ./main.py /app/main.py
COPY ./src /app/src
COPY ./infra/app /app/infra

RUN chmod +x ./infra/entrypoint.sh

ENTRYPOINT ["./infra/entrypoint.sh"]
