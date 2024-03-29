# syntax = docker/dockerfile:experimental
FROM apache/airflow:2.7.2

COPY ./requirements.txt ./

RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}"  -r ./requirements.txt