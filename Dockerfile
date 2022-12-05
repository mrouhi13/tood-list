# BUILDER
FROM python:3.9-alpine as builder

ARG ENVIRONMENT

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apk update && apk add gcc python3-dev musl-dev libc-dev postgresql-dev

COPY ./requirements ./requirements

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements/$ENVIRONMENT.txt

# FINAL
FROM python:3.9-alpine

WORKDIR /app

RUN apk update && apk add gcc make musl-dev libpq

COPY --from=builder /app/wheels /wheels

RUN pip install --no-cache --upgrade pip && pip install --no-cache /wheels/*

COPY ./source ./source
COPY ./entrypoint.sh .

ENTRYPOINT ["/app/entrypoint.sh"]
