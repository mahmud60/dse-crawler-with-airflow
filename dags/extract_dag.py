from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup

# Default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 9, 26),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the main DAG
dag = DAG(
    'extract_and_save_share_prices',
    default_args=default_args,
    description='Insert company data first, then scrape DSE share prices daily',
    schedule_interval=timedelta(days=1),  # Runs daily
)

# Global variables
url = 'https://www.dse.com.bd/latest_share_price_scroll_l.php'
rows = []
baseUrl = "https://www.dse.com.bd/displayCompany.php?name="


# Functions
def fetch_webpage():
    """Fetch the webpage content."""
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

def extract_share_data():
    """Extract data from the fetched HTML for share prices."""
    soup = fetch_webpage()
    table = soup.find('table', {'class': 'table table-bordered background-white shares-table fixedHeader'})
    
    for tr in table.find_all('tr'):
        cols = tr.find_all('td')
        if len(cols) > 0:  # Skip empty rows
            row_data = [td.text.strip() for td in cols]
            rows.append(row_data)
    return rows

def save_share_prices_data():
    """Save extracted share prices data to the PostgreSQL table."""
    hook = PostgresHook(postgres_conn_id='dse_connection')
    extracted_rows = extract_share_data()
    
    insert_query = """
        INSERT INTO company_share_prices (
            company_id, date, latest_trading_price, high_price, low_price, closing_price, ycp, change, trade, value, volume
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        );
    """
    
    for row in extracted_rows:
        try:
            hook.run(insert_query, parameters=(
                row[0], datetime.now(), row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]
            ))
        except Exception as error:
            print(f"Error inserting share prices data: {error}")

# Task 4: Save share prices data
t4 = PythonOperator(
    task_id='save_share_prices_data',
    python_callable=save_share_prices_data,
    dag=dag,
)

t4