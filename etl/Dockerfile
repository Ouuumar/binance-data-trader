FROM python:3.9.4-buster

COPY ./requirements.txt ./
COPY ./init_data.py ./
COPY ./functions.py ./

RUN pip install -U pip && pip install -r ./requirements.txt

CMD python3 init_data.py
