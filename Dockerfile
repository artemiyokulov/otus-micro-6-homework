FROM python:3.8

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY src/openapi_server ./

CMD uvicorn main:app --host 0.0.0.0 --port 80