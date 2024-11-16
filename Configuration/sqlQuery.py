from Configuration.config import *

SIGNUP_TABLE = "user_credential"

def signup_create_query() -> str:
    query = f"""
            CREATE TABLE {SIGNUP_TABLE} (
            id SERIAL PRIMARY KEY,
            date_time VARCHAR,
            email VARCHAR,
            first_name VARCHAR,
            last_name VARCHAR,
            number VARCHAR,
            password VARCHAR,
            verify BOOLEAN,
            user_role VARCHAR
            );
            """
    return query


def signup_insert_query() -> str:
    query =  f"""
        INSERT INTO {SIGNUP_TABLE} (date_time, email, first_name, last_name, number, password, verify, user_role)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
    return query

# This function is resposible for returning a query to check the table exists or not
def is_table_exist_query(table_name: str) -> str:
    query = f"""
                SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_name = '{table_name}'
            );
            """ 
    return query        


# This function is resposible for check the table exists or not 
def is_table_exist(table_name: str) -> bool:
    try:
        pg_cursor = DB_CONNECTION.cursor()
        pg_cursor.execute(is_table_exist_query(table_name), (table_name,))
        exists = pg_cursor.fetchone()[0]
        pg_cursor.close()
        return exists
    except Exception as error:
        logging.error(f"ERROR OCCURED WHILE CHECKING {table_name} EXISTANCE: " f"{error}")
        return False