import os
from functions import *
from binance import Client
from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI, BackgroundTasks

client = Client()
load_dotenv(find_dotenv())
engine = create_con(user=os.environ["MYSQL_USER"], pw=os.environ["MYSQL_PASSWORD"], ip=os.environ["MYSQL_IP"],port=os.environ["MYSQL_PORT"], db=os.environ["MYSQL_DATABASE"])

api = FastAPI(
    title="Binance Klines API",
    description="Get, update abd delete Klines of any symbol you want",
    version="1.0.1",
    openapi_tags=[
    {
        "name": "home",
        "description" : "status function"
    },
    {
        "name" : "data manipulation",
        "description" : "manage klines data"
    }
    ]
)

@api.get("/", tags=["home"])
def status():
    """Return status of the application"""
    return {"status":"working"}


@api.get("/klines/get/symbol/{symbol:str}", tags=["data manipulation"])
def get_all_klines(symbol):
    """Return all symbol's Klines"""
    
    query = engine.execute(text(f"SELECT * FROM historical_klines WHERE symbol = '{symbol}'")).fetchall() 
    return query

@api.get("/klines/get/symbol/{symbol:str}/limit/{limit:int}", tags=["data manipulation"])
def get_all_klines(symbol, limit):
    """Return symbol's Klines with limited rows"""
    
    query = engine.execute(text(f"SELECT * FROM historical_klines WHERE symbol = '{symbol}' LIMIT {limit}")).fetchall() 
    return query


@api.get("/klines/get/symbol/{symbol:str}/from/{from_d:str}/to/{to_d:str}", tags=["data manipulation"])
def get_klines_from(symbol, from_d, to_d):
    """Return symbol's Klines between date range"""

    query = engine.execute(text(f"SELECT * FROM historical_klines WHERE symbol = '{symbol}'\
                         AND open_time >= '{from_d}' AND close_time <= '{to_d}'")).fetchall() 
    return query


@api.get("/klines/delete/symbol/{symbol:str}", tags=["data manipulation"])
def delete_klines(symbol):
    """Delete symbol's Klines"""

    engine.execute(text(f"DELETE FROM historical_klines WHERE symbol = '{symbol}'"))
    return {symbol : f"Deleting {symbol}'s Klines . . ."}


@api.get("/klines/update/symbol/{symbol:str}", tags=["data manipulation"])
async def update_klines(symbol, background_tasks: BackgroundTasks):
    """Call ETL to get and update or push new symbol's Klines"""
    
    background_tasks.add_task(etl, [symbol], client)
    return {symbol : "Pushing in background . . ."}