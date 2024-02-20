import pymysql
from sqlalchemy import create_engine
import pandas as pd
import yfinance as yf
import time
from tqdm import tqdm
import json

with open('env/config.json') as f:
    config = json.load(f)

DB_USER = config['DB_USER']
DB_PASSWORD = config['DB_PASSWORD']
DB_HOST = config['DB_HOST']
DB_NAME = config['DB_NAME']
DB_CHARSET = config['DB_CHARSET']

engine = create_engine(
    f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}')
con = pymysql.connect(user=DB_USER,
                      passwd=DB_PASSWORD,
                      host=DB_HOST,
                      db=DB_NAME,
                      charset=DB_CHARSET)

mycursor = con.cursor()

ticker_list = pd.read_sql("""
select * from ticker
where date = (select max(date) from ticker)
and country = 'United States';
""", con=engine)

query = """
    insert into global_price (Date, High, Low, Open, Close, Volume, `Adj Close`, ticker)
    values (%s, %s,%s,%s,%s,%s,%s,%s) as new
    on duplicate key update
    High = new.High, Low = new.Low, Open = new.Open, Close = new.Close,
    Volume = new.Volume, `Adj Close` = new.`Adj Close`;
"""

error_list = []

for i in tqdm(range(0, len(ticker_list))):

    ticker = ticker_list['Symbol'][i]

    try:
        price = yf.download(ticker, progress=False)

        price = price.reset_index()
        price['ticker'] = ticker

        args = price.values.tolist()
        mycursor.executemany(query, args)
        con.commit()

    except:
        print(ticker)
        error_list.append(ticker)

    time.sleep(2)

engine.dispose()
con.close()
