import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

date = datetime.today().strftime('%d-%m-%Y')

# Step 1: Fetch the webpage content
url = 'https://www.dse.com.bd/displayCompany.php?name=1JANATAMF'
response = requests.get(url)

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

def extract_market_info():
    # Step 4: Extract headers
    header_rows = tables[0].find_all('tr')
    headers = []
    headers.append('Date')
    for tr in header_rows:
        for th in tr.find_all('th'):
            if (len(headers) == 6):
                headers.append('Change %')
            headers.append(th.text.strip())

    # Step 5: Extract table rows
    rows = []
    data = []
    data.append(date)
    for tr in tables[0].find_all('tr'):  # Skip the header row
        cols = tr.find_all('td')
        row_data = [td.text.strip() for td in cols]
        if row_data:
            for row in row_data:
                data.append(row)

    rows.append(data)

    # Step 6: Create a DataFrame with extracted headers and rows
    df = pd.DataFrame(rows, columns= headers)

    # Step 7: Append the extracted data to an existing CSV file
    output_file = '1JANATAMF.csv'
    try:
        # Open the file in append mode and write the DataFrame
        df.to_csv(output_file, mode='a', header=not pd.io.common.file_exists(output_file), index=False)
        print(f'Data has been successfully appended to {output_file}')
    except Exception as e:
        print(f"An error occurred while writing to the CSV file: {e}")

def extract_basic_info():

    # Step 4: Extract headers
    basic_info_header_rows = tables[1].find_all('tr')
    basic_info_headers = []
    basic_info_headers.append('Date')
    for tr in basic_info_header_rows:
        for th in tr.find_all('th'):
            if len(basic_info_headers) < 9:
                basic_info_headers.append(th.text.strip())

    # Step 5: Extract table rows
    basic_info_rows = []
    basic_info_data = []
    basic_info_data.append(date)
    for tr in tables[1].find_all('tr'):  # Skip the header row
        if len(basic_info_data) < 9:
            cols = tr.find_all('td')
            row_data = [td.text.strip() for td in cols]
            if row_data:
                for row in row_data:
                    basic_info_data.append(row)

    basic_info_rows.append(basic_info_data)
    #print(basic_info_headers)
    # Step 6: Create a DataFrame with extracted headers and rows
    df = pd.DataFrame(basic_info_rows, columns= basic_info_headers)

    # Step 7: Append the extracted data to an existing CSV file
    output_file = '1JANATAMF_basic.csv'
    try:
        # Open the file in append mode and write the DataFrame
        df.to_csv(output_file, mode='a', header=not pd.io.common.file_exists(output_file), index=False)
        print(f'Data has been successfully appended to {output_file}')
    except Exception as e:
        print(f"An error occurred while writing to the CSV file: {e}")

extract_basic_info()
#extract_market_info()
