FROM python:3.6-slim
RUN apt-get update && apt-get install gettext --no-install-recommends -y && rm -rf /var/lib/apt/lists/*
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip && pip install pipenv

WORKDIR /src

COPY requirements.txt ./
COPY Pipfile ./
COPY Pipfile.lock ./
RUN pipenv install --system

COPY scripts ./scripts
COPY static ./static
COPY tekis ./tekis

COPY manage.py ./

RUN python manage.py compilemessages

EXPOSE 5000
CMD ["python", "manage.py", "runserver" , "0.0.0.0:5000"]