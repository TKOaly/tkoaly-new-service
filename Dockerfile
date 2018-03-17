FROM ubuntu:16.04
FROM python:3.6
ENV PYTHONUNBUFFERED 1
EXPOSE ${PORT:-8000}
RUN apt-get update && \
    apt-get install -y gettext
RUN mkdir /src
WORKDIR /src
ADD requirements.txt /src/
RUN pip install -U -r requirements.txt
ADD . /src/