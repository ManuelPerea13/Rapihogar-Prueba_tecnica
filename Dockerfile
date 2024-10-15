# syntax=docker/dockerfile:1
FROM python:3.10-slim

RUN apt-get update && apt-get install -y gcc

ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /code/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]