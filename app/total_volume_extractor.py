import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# Step 1: Fetch the webpage content
url = 'https://www.dse.com.bd/php_graph/monthly_graph.php?inst=1JANATAMF&duration=24&type=vol'
response = requests.get(url)

# Step 2: Parse the webpage content
soup = BeautifulSoup(response.content, 'html.parser')

# Step 3: Find the <script> tag containing the graph data
script_tags = soup.find_all('script')

# Step 4: Extract the CSV data from the script tag
csv_data = None
for script in script_tags:
    if 'Dygraph(' in script.text:
        # Use regex to extract the CSV string inside the Dygraph initialization

        match = re.search(r'\"Date,Volume\\n\" \+ (.+?)(?=, {\n)', script.text, re.DOTALL)
        print(match)
        if match:
            csv_data = match.group(1)
            break

if csv_data:
    # Step 5: Clean up the CSV data
    csv_data = csv_data.replace('"', '').replace('\\n', '\n').replace('+', '').strip()
    
    # Convert the CSV string into a list of lines
    csv_lines = csv_data.split('\n')

    # Step 6: Convert to pandas DataFrame
    data = []
    for line in csv_lines:
        date, volume = line.split(',')
        data.append({'Date': date.strip(), 'Volume': int(volume.strip())})

    df = pd.DataFrame(data)

    # Step 7: Save to CSV file
    df.to_csv('graph_data_1JANATAMF.csv', index=False)

    print('Graph data has been successfully extracted and saved to graph_data_1JANATAMF.csv')
else:
    print('Could not find graph data in the webpage.')
