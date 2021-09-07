# pull official base image
FROM python:3.9.1
MAINTAINER vbilous@softserveinc.com

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	TZ=Europe/Kiev \
	LANG=C.UTF-8 \
	APP_HOME=/home/ubuntu/web

WORKDIR $APP_HOME

COPY ./stream/requirements  $APP_HOME/requirements

RUN pip install --upgrade pip \
  && pip install -r $APP_HOME/requirements/production.txt

COPY ./stream/entrypoints /
COPY ./stream $APP_HOME

RUN chmod +x /*.sh # && flake8 .
