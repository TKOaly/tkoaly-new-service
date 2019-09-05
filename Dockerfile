FROM python:3.6-slim

EXPOSE 5000

WORKDIR /src

ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install gettext --no-install-recommends -y && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip && \
    pip install pipenv

COPY requirements.txt Pipfile Pipfile.lock manage.py ./

RUN pipenv install --system

COPY scripts ./scripts
COPY static ./static
COPY tekis ./tekis

RUN python manage.py compilemessages

CMD ["python", "manage.py", "runserver" , "0.0.0.0:5000"]