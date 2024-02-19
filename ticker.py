from sqlalchemy import create_engine
from datetime import datetime
import pymysql
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from datetime import datetime
import math
import pandas as pd
import numpy as np
from tqdm import tqdm
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
nationcode = '5'
url = f'''https://investing.com/stock-screener/?sp=country::
{nationcode}|sector::a|industry::a|equityType::ORD%3Ceq_market_cap;1'''
driver.get(url)

WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
    (By.XPATH, '//*[@id="resultsTable"]/tbody')))

# end_num = driver.find_element(
#     By.CLASS_NAME, value='js-total-results').text
# end_num = math.ceil(int(end_num) / 50)
# Due to the usage of Selenium, it takes so long when it comes to adopt data from the crawled pages.

all_data_df = []

for i in tqdm(range(1, 2)):
    url = f'''https://investing.com/stock-screener/?sp=country::
        {nationcode}|sector::a|industry::a|equityType::ORD%3Ceq_market_cap;{i}'''
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="resultsTable"]/tbody')))
    except:
        time.sleep(1)
        driver.refresh()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="resultsTable"]/tbody')))

    html = BeautifulSoup(driver.page_source, 'lxml')

    html_table = html.select(
        'table.genTbl.openTbl.resultsStockScreenerTbl.elpTbl')
    df_table = pd.read_html(html_table[0].prettify())
    df_table_select = df_table[0][['Name', 'Symbol',
                                   'Exchange',  'Sector', 'Market Cap']]

    all_data_df.append(df_table_select)

    time.sleep(2)

all_data_df_bind = pd.concat(all_data_df, axis=0)

data_country = html.find(class_='js-search-input inputDropDown')['value']
all_data_df_bind['country'] = data_country
all_data_df_bind['date'] = datetime.today().strftime('%Y-%m-%d')
all_data_df_bind = all_data_df_bind[~all_data_df_bind['Name'].isnull()]
all_data_df_bind = all_data_df_bind[all_data_df_bind['Exchange'].isin(
    ['NASDAQ', 'NYSE', 'NYSE Amex'])]
all_data_df_bind = all_data_df_bind.drop_duplicates(['Symbol'])
all_data_df_bind.reset_index(inplace=True, drop=True)
all_data_df_bind = all_data_df_bind.replace({np.nan: None})

driver.quit()

con = pymysql.connect(
    user='root',
    password='Snowcountry12~',
    host='127.0.0.1',
    db='stock_db',
    charset='utf8'
)

mycursor = con.cursor()
query = """
    insert into ticker (Name, Symbol, Exchange, Sector, `Market Cap`, country, date)
    values (%s,%s,%s,%s,%s,%s,%s) as new
    on duplicate key update
    name=new.name,Exchange=new.Exchange,Sector=new.Sector,
    `Market Cap`=new.`Market Cap`; 
"""

args = all_data_df_bind.values.tolist()

mycursor.executemany(query, args)
con.commit()

con.close()

# META Meta
# AAPL Apple
# AMZN Amazon
# NFLX Netflix
# GOOG Google(Alphabet)

# def download_ticker():
#     apple = yf.download('AAPL', progress=False)
#     print(apple.head())
#     google = yf.download('GOOG', progress=False)
#     print(google.head())
