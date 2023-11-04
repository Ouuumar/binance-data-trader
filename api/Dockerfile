# syntax = docker/dockerfile:experimental
FROM python:3.9.4-buster

COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r ./requirements.txt

COPY ./api.py ./

COPY ./functions.py ./

CMD ["uvicorn", "api:api", "--host", "0.0.0.0", "--port", "8000"]