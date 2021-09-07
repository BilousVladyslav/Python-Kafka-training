# pull official base image
FROM python:3.9.1
MAINTAINER vbilous@softserveinc.com

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	TZ=Europe/Kiev \
	LANG=C.UTF-8 \
	APP_HOME=/home/ubuntu/web

RUN apt-get update && apt-get install -y librdkafka-dev \
    && pip install --upgrade pip

WORKDIR $APP_HOME

COPY ./consumer/requirements  $APP_HOME/requirements
COPY ./consumer/entrypoints /

RUN pip install --upgrade pip \
  && pip install -r $APP_HOME/requirements/production.txt

COPY ./consumer $APP_HOME

RUN chmod +x /*.sh # && flake8 .
