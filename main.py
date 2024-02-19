import numpy as np
import pymysql
import pandas as pd
import ticker
from sqlalchemy import create_engine
from datetime import datetime
from IPython.core.interactiveshell import InteractiveShell
import FinanceDataReader as fdr
from tqdm import tqdm

#  for american fed data
import pandas_datareader as web


def db_connect():
    engine = create_engine(
        'mysql+pymysql://root:Snowcountry12~@127.0.0.1:3306/stock_db')
    con = pymysql.connect(
        user='root',
        password='Snowcountry12~',
        host='127.0.0.1',
        db='stock_db',
        charset='utf8'
    )
    mycursor = con.cursor()

    con.close()


def fed_constant_maturity():
    t10y2y = web.DataReader('T10Y2Y', 'fred', start='2002-01-01')
    t10y3m = web.DataReader('T10Y3M', 'fred', start='2002-01-01')

    rate_diff = pd.concat([t10y2y, t10y3m], axis=1)
    rate_diff.columns = ['10Y-2Y', '10Y-3M']
    print(rate_diff.tail())


def setting_display():  # Setting for the display
    InteractiveShell.ast_node_interactivity = "all"
    pd.set_option('display.float_format', lambda x: '%.3f' % x)
    pd.set_option('display.max_columns', None)


# setting_display()
# fed_constant_maturity()


def main():
    # db_connect()
    ticker


if __name__ == '__main__':
    main()
