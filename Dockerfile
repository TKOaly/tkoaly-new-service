FROM alpine:3.5
RUN apk add --no-cache gettext
FROM python:3.6-slim
ENV PYTHONUNBUFFERED 1
RUN mkdir /src
WORKDIR /src
ADD . /src/
RUN pip install --upgrade pip && pip install pipenv && pipenv install --system