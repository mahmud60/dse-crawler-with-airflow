import requests
from bs4 import BeautifulSoup
import psycopg2
from config import load_config
from datetime import datetime

# Step 1: Fetch the webpage
url = 'https://www.dse.com.bd/latest_share_price_scroll_l.php'
response = requests.get(url)

# Step 2: Parse the webpage content
soup = BeautifulSoup(response.content, 'html.parser')

# Step 3: Find the table with the latest share prices
table = soup.find('table', {'class': 'table table-bordered background-white shares-table fixedHeader'})

# Step 4: Extract headers
headers = []
for th in table.find_all('th'):
    headers.append(th.text.strip())

# Step 5: Extract data rows
rows = []
config = load_config()

def extract_data():
    for tr in table.find_all('tr'):
        cols = tr.find_all('td')
        if len(cols) > 0:  # Skip empty rows
            row_data = []
            for td in cols:
                row_data.append(td.text.strip())
            rows.append(row_data)
    return rows

def create_table():
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                        CREATE TABLE IF NOT EXISTS company_share_prices (
                                id SERIAL,
                                company_id INTEGER NOT NULL,
                                date DATE,
                                latest_trading_price VARCHAR(50),
                                low_price VARCHAR(50),
                                high_price VARCHAR(50),
                                closing_price VARCHAR(50),
                                ycp VARCHAR(50),
                                change VARCHAR(10),
                                trade VARCHAR(50),
                                value VARCHAR(50),
                                volume VARCHAR(50),
                                PRIMARY KEY(company_id, id),
                                FOREIGN KEY(company_id)
                                    REFERENCES company_list(company_id)
                                    ON UPDATE CASCADE ON DELETE CASCADE
                            )
                    """)
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)

def save_data():
    for row in rows:
        try:
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                               INSERT INTO company_share_prices (company_id, date, latest_trading_price, high_price, low_price, closing_price, ycp, change, trade, value, volume) 
                               VALUES((Select company_id FROM company_list WHERE company_trade_name LIKE %s), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                               (row[1], datetime.now(), row[2], row[3], row[4],row[5], row[6], row[7], row[8], row[9], row[10]))
        except(Exception, psycopg2.DatabaseError) as error:
            print("Error")
            print(error)

create_table()
extract_data()
save_data()