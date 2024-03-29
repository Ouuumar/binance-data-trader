CREATE DATABASE IF NOT EXISTS binance;

USE binance;

CREATE TABLE IF NOT EXISTS historical_klines(
                open_time DATETIME NOT NULL,
                open FLOAT,
                high FLOAT,
                low FLOAT,
                close FLOAT,
                volume FLOAT,
                close_time DATETIME,
                number_of_trades BIGINT,
                symbol VARCHAR(12) NOT NULL,
                PRIMARY KEY (open_time, symbol));