import time
from binance import Client
import pathlib
import sys 
from dotenv import load_dotenv
from functions import *

load_dotenv()
# current_file = pathlib.Path(__file__).parent.resolve() 
# sys.path.append(f"{current_file}/..")

# from func.functions import *

if __name__ == "__main__":

    client = Client()
    time.sleep(5)
    etl(client=client)