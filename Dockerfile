FROM python:3.8

WORKDIR /usr/src/app

COPY . .

RUN apt-get update && apt-get install -y g++ unixodbc-dev && \
    apt-get install -y build-essential libssl-dev libffi-dev python3-dev
