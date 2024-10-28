# Importing some useful packages 
import os
import logging
import psycopg2
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()


# Current Date and Time
def date_time():
    CURRENT_DATE = datetime.now().strftime('%Y-%m-%d')
    CURRENT_TIME = datetime.now().strftime('%H:%M:%S')
    return CURRENT_DATE, CURRENT_TIME

# Setting Up Logger instead of print()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S")

# Defining Database parameters for Postgres SQL
DB_PARAMETER = {
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USERNAME'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT')
    }

# Email sending credentials
EMAIL_SENDER = os.getenv('EMAIL_SENDER')
EMAIL_SENDER_PASSWORD = os.getenv('EMAIL_SENDER_PASSWORD')

# Building a connection with Postgres SQL 
def db_connection():
        try:
            connection = psycopg2.connect(**DB_PARAMETER)
            return connection
        except Exception as e:
            logging.error(f"Error while connecting to database: {str(e)}")
            
# This varriable stores database connection            
DB_CONNECTION = db_connection()
