# Dhaka Stock Exchange Data Crawler

This project automates the process of crawling stock market data from the Dhaka Stock Exchange (DSE) and stores it in a PostgreSQL database. Using **Apache Airflow** for orchestration and **Python** for data scraping, the pipeline ensures reliable and scheduled updates of stock data.

## Features:
- **Data Scraping**: Extracts real-time stock prices and other relevant financial data from the DSE website.
- **Data Storage**: Saves the crawled data into a PostgreSQL database, making it easily accessible for further analysis.
- **Apache Airflow**: Automates and schedules the data pipeline, ensuring the system runs at defined intervals or based on specific triggers.
- **Modular Design**: Easily extendable to add more sources or process different kinds of stock data.

## Technologies:
- **Apache Airflow**: For scheduling and workflow orchestration.
- **Python**: Used for web scraping and data processing.
- **PostgreSQL**: The database for storing and querying stock data.
- **Docker** (optional): For containerized deployment and easy setup.

## How It Works:
1. Apache Airflow triggers a scheduled task to scrape data from the Dhaka Stock Exchange website.
2. The Python script fetches and processes the data.
3. The processed data is stored in a PostgreSQL database for future use.
4. Logs and error handling ensure smooth operation and reliability.

## Usage:
1. Clone the repository.
2. Configure PostgreSQL and Airflow settings.
3. Run the project using Airflow to schedule regular stock data updates.

This project provides a scalable solution for tracking Dhaka Stock Exchange data efficiently.
