FROM python:3.7.6-slim-buster
LABEL maintainer="Dipto Karmakar"
ENV PYTHONUNBUFFERED 1
COPY requirements.txt /requirements.txt
COPY requirements-dev.txt /requirements-dev.txt
RUN apt-get update && apt-get install -y --no-install-recommends \
  postgresql-client-11 gcc libc-dev postgresql-server-dev-11 \
  && rm -rf /var/lib/apt/lists/*
RUN pip install -r /requirements.txt
RUN pip install -r /requirements-dev.txt

RUN mkdir /src
WORKDIR /src
COPY ./src /src

RUN adduser user
USER user
