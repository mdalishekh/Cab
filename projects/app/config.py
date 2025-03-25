import psycopg2
from psycopg2.extensions import connection as Connection

DB_PARAMETER = {
        'dbname': 'postgres',
        'user': 'postgres',
        'password': 'postgres',
        'host': 'localhost',
        'port': 5432
    }

# Building a connection with Postgres SQL 
def db_connection():
    try:
        connection: Connection = psycopg2.connect(**DB_PARAMETER)
        return connection
    except Exception as e:
        return None