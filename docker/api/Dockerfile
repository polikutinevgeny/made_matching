FROM python:3.8-slim-buster

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y -q build-essential

COPY ./requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip && pip --no-cache-dir install -r /tmp/requirements.txt

WORKDIR /

COPY ./fasttext.bin /fasttext.bin

COPY ./matching /matching

CMD ["gunicorn", "matching.api:app", "--workers", "2", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:80", "--timeout", "0"]
