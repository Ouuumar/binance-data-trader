from statsmodels.tsa.arima.model import ARIMA
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from dotenv import load_dotenv
from datetime import timedelta, date
from airflow import DAG
import pandas as pd
import numpy as np
import pathlib
import logging
import pickle

import sys 

TODAY = date.today()

load_dotenv()

current_file = pathlib.Path(__file__).parent.resolve() 
sys.path.append(f"{current_file}/..")
from func.functions import *

logging.basicConfig(level=logging.INFO)

DAG_ID = "arima_dag"
TODAY = date.today()

args = {
    "owner" : "Omar Allouache",
    "retries" : 0,
    "retry_delay" : timedelta(minutes=2),
    "start_date" : days_ago(1)
}

def train_model():
    model="ttt"
    # from pathlib import Path
    with open("/opt/airflow/models/arima_model.pkl", "wb") as f:
        pickle.dump(model, f)
    # path = Path("./models/model.pkl")
    # with open(path.parent.absolute(), "wb") as f:
    #     pickle.dump(model, f)
    # print(path.parent.absolute())

ml_dag = DAG(dag_id=DAG_ID, 
          description="train and save ml model",
          default_args=args,
          schedule_interval=None,
          )

get_data = PythonOperator(
    task_id='ml_process', 
    python_callable=train_model,
    dag=ml_dag
    )