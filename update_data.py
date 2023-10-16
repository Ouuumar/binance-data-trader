from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
from binance import Client
from airflow import DAG
import functions.functions
import requests
import pathlib
import sys 

# current_file = pathlib.Path(__file__).parent.resolve() 
# sys.path.append(f"{current_file}/../..")
# from etl.functions import etl

client = Client()

symbols = requests.get("http://172.1.1.5:8000/klines/list/symbol").json()

args = {
    "owner" : "Omar Allouache",
    "retries" : 2,
    "retry_delay" : timedelta(minutes=2),
    "start_date" : days_ago(1)
}

dag = DAG(dag_id="update_data", 
          description="update avalaible symbols in db",
          default_args=args,
          schedule_interval="@daily",
          )

task = PythonOperator(task_id='hello_task', python_callable=functions.etl, op_args=[symbols, client], dag=dag)

task