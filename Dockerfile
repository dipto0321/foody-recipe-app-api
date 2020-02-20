FROM python:3.7.6-slim-buster
LABEL maintainer="Dipto Karmakar"
ENV PYTHONUNBUFFERED 1 
RUN pip install pipenv
COPY Pipfile* /
RUN pipenv lock --requirements > requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /src
WORKDIR /src
COPY ./src /src

RUN adduser user
USER user
