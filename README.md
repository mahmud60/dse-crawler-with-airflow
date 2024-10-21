# Dhaka Stock Exchange Data Crawler

This project automates the process of crawling stock market data from the Dhaka Stock Exchange (DSE) and stores it in a PostgreSQL database. The entire pipeline is orchestrated using **Apache Airflow** and is containerized with **Docker** for easy deployment and scalability.

## Features:
- **Data Scraping**: Extracts real-time stock prices and financial data from the DSE website.
- **Data Storage**: Stores the crawled data in a PostgreSQL database for easy querying and analysis.
- **Apache Airflow**: Manages task scheduling and orchestration for automated and reliable data extraction.
- **Docker**: Containerized setup ensures easy deployment and consistent environments across different platforms.
- **Modular Design**: Easily extendable to add new data sources or customize the scraping and processing logic.

## Technologies:
- **Apache Airflow**: Workflow orchestration and scheduling.
- **Python**: Web scraping and data processing.
- **PostgreSQL**: Database for storing and managing stock data.
- **Docker**: Containers for seamless deployment and environment consistency.

## How It Works:
1. **Docker** sets up the required environment for Airflow, Python, and PostgreSQL.
2. **Apache Airflow** schedules and triggers tasks to scrape stock data from the DSE website.
3. The **Python** script fetches, processes, and validates the data.
4. The processed data is saved in the **PostgreSQL** database.
5. Logs and monitoring provide insights into task execution and potential issues.

## Usage:
1. Clone the repository.
2. Use Docker to build and start the containers (Airflow, PostgreSQL, etc.).
3. Configure PostgreSQL and Airflow settings.
4. Run the Airflow scheduler to automate stock data scraping at regular intervals.

This project provides a reliable and scalable solution for scraping and storing Dhaka Stock Exchange data using Docker for containerization.
