FROM python:3.9.4-buster

COPY ./requirements.txt ./
COPY ./live_viewing.py ./

RUN pip install -U pip && pip install -r ./requirements.txt

EXPOSE 8050

CMD python3 live_viewing.py
