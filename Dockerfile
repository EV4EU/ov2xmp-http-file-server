FROM python:3.10-slim

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

RUN mkdir /files

EXPOSE 80

CMD sanic http-server:app --host=0.0.0.0 --port=80