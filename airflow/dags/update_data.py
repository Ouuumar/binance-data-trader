from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
from binance import Client
from airflow import DAG
from func.functions import *
# import pathlib
# import sys 

# current_file = pathlib.Path(__file__).parent.resolve() 
# sys.path.append(f"{current_file}/../..")
# from etl.functions import etl

client = Client()

args = {
    "owner" : "Omar Allouache",
    "retries" : 0,
    "retry_delay" : timedelta(minutes=2),
    "start_date" : days_ago(1)
}

update_data_dag = DAG(dag_id="update_data", 
          description="update avalaible symbols in db",
          default_args=args,
          schedule_interval="@daily",
          )

update_data = PythonOperator(
    task_id='update_data', 
    python_callable=etl,
    op_args=[client],
    dag=update_data_dag
    )

update_data
