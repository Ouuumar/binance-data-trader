import os
import datetime
import pandas as pd
from dateutil import parser
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text


def get_hist_klines(conn, symbol, table, client_interval, client): 
    """ Return the symbol's historical klines data from Binance
    Parameters 
    ---------------------------------------
        con : Engine()
                the engine/connection of MySQL
        symbol : str
                symbol (pair of crypto)
        client_interval : str
                interval of klines
    Return
    ---------------------------------------
            client.get_historical_klines() : json
                The json symbol data klines
    """
    # Check if no symbol's data in table, download data from the oldest date available e.g 1 Aug 2017 (Binance founded date)
    if ((conn.execute(text(f"SELECT COUNT(*) FROM {table} WHERE symbol = '{symbol}'")).scalar() == 0)):
        print(f"No data for {symbol}, currently getting {symbol} data from 1 Aug 2017 ...")
        return client.get_historical_klines(symbol, client_interval, "1 Aug 2017")
    else :
        # Get the most recent date of the data if the table is not empty in order to download from the most recent date
        most_recent_date_in_db = (conn.execute(text(f"SELECT max(open_time) FROM {table} WHERE\
        symbol = '{symbol}'"))).scalar()
        one_hour_from_db_date= str(datetime.now() + timedelta(hours=1))[:19] # Select only %y-%m-%d %H:%M:%S and add 1 hour
        one_hour_from_db_date = parser.parse(one_hour_from_db_date) # Parse the date
        print(f"{symbol} data already present, getting {symbol} data from {most_recent_date_in_db} + 1 hour if exists")
        return client.get_historical_klines(symbol, client_interval, str(one_hour_from_db_date))

def create_con(user, pw, ip, port, db):
        """ Return the engine (the connection) to interact with MySQL
        Parameters 
        ---------------------------------------
                user : str
                        the user name
                pw : str
                        the user password
                db : str
                        the database name
        Return
        ---------------------------------------
                engine : Engine(mysql+pymysql://{user}:{pw}@localhost)
        """
        engine = create_engine(f"mysql+pymysql://{user}:{pw}@{ip}:{port}/{db}")
        print(f"Connection at {engine} : created !")
        return engine

def export_data(conn, data, schema, table):
        """ Load data into MySQL
        Parameters 
        ---------------------------------------
                con : Engine()
                        the engine/connection of MySQ
                data : pandas.DataFrame()
                        symbols data
                table : str
                        the table name
        Return
        ---------------------------------------
                Nothing
        """
        data.to_sql(con=conn, schema=schema, name=table, if_exists="append")
        

def process_hist_data(data, symbol):
    """ Return DataFrame of the data processed 
    Parameters 
    ---------------------------------------
            data : json
                    symbol data
            symbol : str
                    symbol (pair of crypto)
    Return
    ---------------------------------------
            df : pandas.Dataframe()
                symbol data processed into DataFrame
    """
    # Return processed json klines data into pandas dataframe
    df = pd.DataFrame(data, columns=["open_time", "open", "high", "low", "close", "volume","close_time",\
    "quote_asset_volume", "number_of_trades", "taker_buy_base_asset_volume","taker_buy_quote_asset_volume","ignore"])
    
    df.drop("ignore",axis=1, inplace=True)
    df['open_time'] = pd.to_datetime(df['open_time']/1000, unit='s')
    df['close_time'] = pd.to_datetime(df['close_time']/1000, unit='s')

    numeric_columns = ['open', 'high', 'low', 'close', 'volume', 'quote_asset_volume', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume']
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, axis=1)
    
    df.set_index("open_time", inplace=True)

    df["symbol"] = symbol
    df = df.astype({"symbol" : "string"})
    return df


def etl(symbols, client):
    """ Extract, transform and load the symbol's klines data processed
    Parameters 
    ---------------------------------------
        symbols : list
                the list of symbol to treat
    Return
    ---------------------------------------
        Nothing
    """
    conn = create_con(user=os.environ["MYSQL_USER"], pw=os.environ["MYSQL_PASSWORD"], ip=os.environ["MYSQL_IP"],port=os.environ["MYSQL_PORT"], db=os.environ["MYSQL_DATABASE"])
    for crypto in symbols:  
        historical_data = get_hist_klines(conn, str(crypto), os.environ["KLINES_TABLE"], client.KLINE_INTERVAL_1HOUR, client=client)
        print(f"{crypto} downloaded")
        df = process_hist_data(historical_data, crypto)
        print(f"{crypto} processed")
        export_data(conn=conn, data=df, schema=os.environ["MYSQL_DATABASE"], table=os.environ["KLINES_TABLE"])
        print(f"{crypto} pushed to database")