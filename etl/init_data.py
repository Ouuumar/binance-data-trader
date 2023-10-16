import time
from functions import *
from binance import Client

if __name__ == "__main__":

    client = Client()
    time.sleep(5)
    etl(["SHIBUSDT"], client=client)