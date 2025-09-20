FROM python:3.12-slim

WORKDIR /projecthome30.1

RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

RUN ./venv/bin/pip install -r requirements.txt

COPY . .

EXPOSE 8000