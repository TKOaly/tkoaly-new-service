FROM python:3.6-slim
RUN apt-get update && apt-get install gettext --no-install-recommends -y && rm -rf /var/lib/apt/lists/*
ENV PYTHONUNBUFFERED 1
RUN mkdir /src
WORKDIR /src
ADD . /src/
EXPOSE 5000
RUN pip install --upgrade pip && pip install pipenv && pipenv install --system
CMD ["python", "manage.py", "runserver" , "0.0.0.0:5000"]