FROM python:3.8.3-slim

RUN apt-get update

COPY . /app/api
WORKDIR /app

RUN python -m pip install --upgrade pip
RUN pip install -r api/requirenments.txt

EXPOSE 1984