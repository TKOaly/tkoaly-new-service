FROM python:3.6-slim
RUN apt-get update && apt-get install gettext -y
ENV PYTHONUNBUFFERED 1
RUN mkdir /src
WORKDIR /src
ADD . /src/
RUN pip install --upgrade pip && pip install pipenv && pipenv install --system