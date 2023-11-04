# syntax = docker/dockerfile:experimental
FROM python:3.9.4-buster

COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r ./requirements.txt
    
COPY ./live_viewing.py ./

EXPOSE 8050

CMD python3 live_viewing.py
