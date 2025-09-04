FROM python:3.12

ENV SECRET_KEY=os.getenv("SECRET_KEY")
ENV CELERY_RESULT_BACKEND=os.getenv("CELERY_RESULT_BACKEND")
ENV CELERY_BROKER_URL=os.getenv("CELERY_BROKER_URL")

WORKDIR /projecthome30.1

RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000