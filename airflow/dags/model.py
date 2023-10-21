from sklearn.model_selection import train_test_split
from airflow.operators.python import PythonOperator
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from airflow.utils.dates import days_ago
from sklearn.metrics import r2_score
from airflow.models import DagModel
from datetime import timedelta
from binance import Client
from datetime import date
from airflow import DAG
import pandas as pd
import pathlib
import pickle 
import logging
import sys 
from dotenv import load_dotenv

load_dotenv()

current_file = pathlib.Path(__file__).parent.resolve() 
sys.path.append(f"{current_file}/..")
from func.functions import *

logging.basicConfig(level=logging.INFO)

DAG_ID = "ml_dag"
TODAY = date.today()

args = {
    "owner" : "Omar Allouache",
    "retries" : 0,
    "retry_delay" : timedelta(minutes=2),
    "start_date" : days_ago(1)
}

def ml_process(task_instance):
    conn = create_con(user=os.environ["MYSQL_USER"], pw=os.environ["MYSQL_PASSWORD"], ip=os.environ["MYSQL_IP"],port=os.environ["MYSQL_PORT"], db=os.environ["MYSQL_DATABASE"])
    df = pd.read_sql("SELECT * FROM historical_klines", con=conn)
    logging.info(df.head())
    X = df[["symbol","high", "low", "close", "volume", "quote_asset_volume", "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume"]]
    X = pd.get_dummies(X, columns=["symbol"])
    logging.info(X.head())
    y = df[["open"]]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)
    scaler = MinMaxScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    logging.info("Coefficient of determination: %.2f" % r2)

    task_instance.xcom_push(
    key="r2_score_lr",
    value= r2
    )

    with open(f"./model/lr_model_{TODAY}.pkl", "wb") as f:
        pickle.dump(model, f)


ml_dag = DAG(dag_id=DAG_ID, 
          description="train and save ml model",
          default_args=args,
          schedule_interval=None,
          )

get_data = PythonOperator(
    task_id='ml_process', 
    python_callable=ml_process,
    dag=ml_dag
    )