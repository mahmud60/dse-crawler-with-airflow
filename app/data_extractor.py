from bs4 import BeautifulSoup
import requests
from datetime import datetime
from config import load_config
from extractor import extract_data
import psycopg2

date = datetime.today().strftime('%d-%m-%Y')

config = load_config()

def company_list():
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("Select * from company_list")
                rows = cur.fetchall()
                return rows
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)

def create_table():
    commands = (        
                """CREATE TABLE IF NOT EXISTS company_basic_info (
                    id SERIAL,
                    company_id INTEGER NOT NULL,
                    date DATE,
                    authorized_capital VARCHAR(50),
                    paid_up_capital VARCHAR(50),
                    type_of_instrument VARCHAR(100),
                    face_per_value VARCHAR(10),
                    market_lot FLOAT,
                    total_no_outstanding_securities VARCHAR(50),
                    sector VARCHAR(100),
                    PRIMARY KEY (company_id,id),
                    FOREIGN KEY (company_id)
                        REFERENCES company_list (company_id)
                        ON UPDATE CASCADE ON DELETE CASCADE
                    )
                """,
                """CREATE TABLE IF NOT EXISTS company_market_info (
                        id SERIAL,
                        company_id INTEGER NOT NULL,
                        date DATE,
                        last_trading_price VARCHAR(50),
                        closing_price VARCHAR(50),
                        last_update VARCHAR(20),
                        day_range VARCHAR(20),
                        change VARCHAR(20),
                        change_percentage VARCHAR(20),
                        day_value VARCHAR(20),
                        weeks_moving_range VARCHAR(20),
                        opening_price VARCHAR(20),
                        day_volume VARCHAR(50),
                        adjusted_opening_price VARCHAR(50),
                        day_trade VARCHAR(20),
                        yesterday_closing_price VARCHAR(20),
                        market_capitalization VARCHAR(50),
                        PRIMARY KEY(company_id, id),
                        FOREIGN KEY (company_id)
                            REFERENCES company_list(company_id)
                            ON UPDATE CASCADE ON DELETE CASCADE
                    )
                """)
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                for command in commands:
                    cur.execute(command)
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)

companies = company_list()

def extract_and_save_company_basic_data():
    for company in companies:
        response = requests.get(company[2])

        # Check if the request was successful
        if response.status_code != 200:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
            exit()

        # Step 2: Parse the webpage content
        soup = BeautifulSoup(response.content, 'html.parser')
        tables = soup.find_all('table', {'class': 'table table-bordered background-white'})

        if not tables:
            print("No data tables found on the page.")
            exit()

        # Step 4: Extract headers
        basic_info_header_rows = tables[1].find_all('tr')
        basic_info_headers = []
        basic_info_headers.append('Date')
        for tr in basic_info_header_rows:
            for th in tr.find_all('th'):
                if len(basic_info_headers) < 9:
                    basic_info_headers.append(th.text.strip())

        # Step 5: Extract table rows
        basic_info_data = []
        basic_info_data.append(date)
        for tr in tables[1].find_all('tr'):  # Skip the header row
            if len(basic_info_data) < 9:
                cols = tr.find_all('td')
                row_data = [td.text.strip() for td in cols]
                if row_data:
                    for row in row_data:
                        if row == '-':
                            row = 0
                        basic_info_data.append(row)
        try:
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                            INSERT INTO company_basic_info (date, authorized_capital, paid_up_capital, type_of_instrument, face_per_value, market_lot,
                                total_no_outstanding_securities, sector, company_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                            (datetime.now(), basic_info_data[1], basic_info_data[3], basic_info_data[4], basic_info_data[5],
                            basic_info_data[6], basic_info_data[7], basic_info_data[8], company[0]))
        except (psycopg2.DatabaseError, Exception) as error:
            print("error")
            print(error)

def extract_and_save_company_market_info():
    for company in companies:
        response = requests.get(company[2])

        # Check if the request was successful
        if response.status_code != 200:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
            exit()

        # Step 2: Parse the webpage content
        soup = BeautifulSoup(response.content, 'html.parser')
        tables = soup.find_all('table', {'class': 'table table-bordered background-white'})
        print("function")
        if not tables:
            print("No data tables found on the page.")
            exit()

        # Step 5: Extract table rows
        market_data = []
        for tr in tables[0].find_all('tr'):  # Skip the header row
            cols = tr.find_all('td')
            row_data = [td.text.strip() for td in cols]
            if row_data:
                for row in row_data:
                    market_data.append(row)
            print(market_data)
        try:
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                                INSERT INTO company_market_info (date, last_trading_price, closing_price, last_update, day_range, change,
                                change_percentage, day_value, weeks_moving_range, opening_price, day_volume, adjusted_opening_price, day_trade, yesterday_closing_price
                                , market_capitalization, company_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                            (datetime.now(), market_data[0], market_data[1], market_data[2], market_data[3],market_data[4], market_data[5],
                            market_data[6], market_data[7], market_data[8], market_data[9],market_data[10], market_data[11], market_data[12], market_data[13], company[0]))
        except (psycopg2.DatabaseError, Exception) as error:
            print("error")
            print(error)

#create_table()
#extract_and_save_company_basic_data() 
extract_and_save_company_market_info()
