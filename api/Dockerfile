FROM python:3.9.4-buster

COPY ./requirements.txt ./
COPY ./api.py ./
COPY ./functions.py ./

RUN pip install -U pip && pip install -r ./requirements.txt

CMD ["uvicorn", "api:api", "--host", "0.0.0.0", "--port", "8000"]