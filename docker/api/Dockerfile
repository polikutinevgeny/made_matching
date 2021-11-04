FROM python:3.8-slim

COPY ./requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip && pip --no-cache-dir install -r /tmp/requirements.txt

WORKDIR /

COPY ./ft_native_300_ru_wiki_lenta_lemmatize.bin /ft_native_300_ru_wiki_lenta_lemmatize.bin

COPY ./matching /matching

CMD ["uvicorn", "matching.api:app", "--host", "0.0.0.0", "--port", "80"]
