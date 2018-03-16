FROM ubuntu:14.04
FROM python:2
EXPOSE 8000
RUN apt-get update && \
    apt-get install -y gettext
RUN mkdir /tekis
WORKDIR /tekis
ADD requirements.txt /tekis/
RUN pip install -r /tekis/requirements.txt
COPY . /tekis
RUN python manage.py migrate
RUN python manage.py compilemessages