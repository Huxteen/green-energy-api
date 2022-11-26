FROM python:3.8-slim
LABEL website="Husteen Internet Solutions"

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

COPY ./requirements.txt /requirements.txt
RUN python -m pip install --upgrade pip

RUN python -m pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN useradd -ms /bin/bash user
USER user
