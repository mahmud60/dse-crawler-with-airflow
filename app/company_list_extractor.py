import psycopg2
from config import load_config
from extractor import extract_data

baseUrl = "https://www.dse.com.bd/displayCompany.php?name="

company_data = extract_data()

def create_table():
    """ Create tables in the PostgreSQL database"""
    command = (
        """
        CREATE TABLE IF NOT EXISTS company_list (
            company_id SERIAL PRIMARY KEY,
            company_trade_name VARCHAR(255) NOT NULL,
            company_url VARCHAR(255) NOT NULL,
            UNIQUE(company_trade_name)
        )
        """)
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # execute the CREATE TABLE statement
                cur.execute(command)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def insert_company_data():
    for data in company_data:
        url = baseUrl + data[1]
        try:
            config = load_config()
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                            INSERT INTO company_list (company_trade_name, company_url) VALUES (%s, %s)
                        """, (data[1], url))
        except (psycopg2.DatabaseError, Exception) as error:
            print(error)

create_table()
insert_company_data()
