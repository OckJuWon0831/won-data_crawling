from sqlalchemy import create_engine
import pymysql
import pandas as pd
from yahooquery import Ticker
import time
from tqdm import tqdm
import numpy as np
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

query_fs = """
    insert into global_fs (ticker, date, account, value, freq)
    values (%s,%s,%s,%s,%s) as new
    on duplicate key update
    value = new.value;
"""

error_list = []

for i in tqdm(range(0, len(ticker_list))):

    ticker = ticker_list['Symbol'][i]

    try:

        data = Ticker(ticker)

        data_y = data.all_financial_data(frequency='a')
        data_y.reset_index(inplace=True)
        data_y = data_y.loc[:, ~data_y.columns.isin(
            ['periodType', 'currencyCode'])]
        data_y = data_y.melt(id_vars=['symbol', 'asOfDate'])
        data_y = data_y.replace([np.nan], None)
        data_y['freq'] = 'y'
        data_y.columns = ['ticker', 'date', 'account', 'value', 'freq']

        data_q = data.all_financial_data(frequency='q')
        data_q.reset_index(inplace=True)
        data_q = data_q.loc[:, ~data_q.columns.isin(
            ['periodType', 'currencyCode'])]
        data_q = data_q.melt(id_vars=['symbol', 'asOfDate'])
        data_q = data_q.replace([np.nan], None)
        data_q['freq'] = 'q'
        data_q.columns = ['ticker', 'date', 'account', 'value', 'freq']

        data_fs = pd.concat([data_y, data_q], axis=0)

        args = data_fs.values.tolist()
        mycursor.executemany(query_fs, args)
        con.commit()

    except:
        print(ticker)
        error_list.append(ticker)

    time.sleep(2)

engine.dispose()
con.close()
