from configuration.config import *
from Database.LoginVerifier import *

# Table name for Database
SIGNUP_TABLE = "auth_details"
VEHICLE_PRICING = "vehicle_pricing"
CAB_BOOKING_TABLE = "ride_booking"
#

# Create table for user credentials
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

# Insert query for user credential
def signup_insert_query() -> str:
    query =  f"""
        INSERT INTO {SIGNUP_TABLE} 
        (date_time, email, first_name, last_name, number, password, verify, user_role)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
    return query


# Create query for cab booking table with foreign key
def booking_create_query()-> str:
    query = f"""
            CREATE TABLE {CAB_BOOKING_TABLE} (
            id SERIAL PRIMARY KEY,
            date VARCHAR,
            time VARCHAR,
            auth_id INT REFERENCES {SIGNUP_TABLE}(id) ON DELETE CASCADE,
            pickup_address VARCHAR,
            drop_address VARCHAR,
            distance VARCHAR,
            pickup_coordinates  DOUBLE PRECISION[],
            drop_coordinates  DOUBLE PRECISION[],
            vehicle_code VARCHAR,
            ride_fair float,
            payment_status BOOL
            );
            """
    return query

# Insert query for cab booking table 
def booking_insert_query()-> str:
    query = f"""
            INSERT INTO {CAB_BOOKING_TABLE} (
            date,
            time,
            auth_id,
            pickup_address,
            drop_address,
            distance,
            pickup_coordinates,
            drop_coordinates,
            vehicle_code,
            ride_fair,
            payment_status
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
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
        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute(is_table_exist_query(table_name), (table_name,))
        exists = cursor.fetchone()[0]
        cursor.close()    
        connection.close() 
        return exists
    except Exception as error:
        logging.error(f"ERROR OCCURED WHILE CHECKING {table_name} EXISTANCE: " f"{error}")
        return False
    
    
# This function is responsible for Verifying user in datable
def set_verify_true(email: str) -> bool:
    try:
        query = f"""
                Update user_credential
                set verify = True where email = %s
                """    
        connection = db_connection()
        pg_cursor = connection.cursor()        
        pg_cursor = connection.cursor()
        pg_cursor.execute(query, (email,))
        connection.commit()
        pg_cursor.close()
        return True
    except Exception as error:
        logging.error(error)  
        return False  
    
    
# This function check if user email exist or not
def is_user_exist(email: str) -> bool:
    """
    This function is intended to check if the user with given email exist or not.
    
    Args
    -----
        (str) : `email` User email.
        
    Returns
    --------
        (bool) : Returns `True` or `False`    
    """
    
    try:
        query = f"""
                SELECT EXISTS 
                (SELECT 1 FROM {SIGNUP_TABLE} WHERE email = %s)
                """ 
        connection = db_connection()           
        cursor = connection.cursor()
        cursor.execute(query, (email,))
        exists = cursor.fetchone()[0]
        cursor.close()     
        connection.close() 
        return exists
    except Exception as error:
        logging.error("Error occurred fetching user existance")
        logging.error(error)
        return False
        
# This function check if user is verified or not
def is_user_verified(email: str) -> bool :
    """
    This function is intended to check if the user with given email verified or not.
    
    Args
    -----
        (str) : `email` User email.
        
    Returns
    --------
        (bool) : Returns `True` or `False`
    """
    try:
        query = f"""
                SELECT verify FROM {SIGNUP_TABLE} 
                WHERE email = %s
                """
        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute(query, (email,))
        is_verified = cursor.fetchone()[0]
        cursor.close()     
        connection.close() 
        return is_verified
    except Exception as error:
        logging.error("Error occurred while fetching user exist or not")
        logging.error(error)
        return False
        
        
# This fucntion return password fetching query
def fetch_password_query() -> str:
    query = f"""
            SELECT password from {SIGNUP_TABLE} 
            where email = %s
            """   
    return query


# Getting first name corresponding to email
def get_first_name(email: str) -> str:
    try:
        query = f"""
                SELECT first_name FROM {SIGNUP_TABLE}
                WHERE email = %s
                """
        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute(query, (email,))
        first_name = "".join(cursor.fetchone())
        return first_name
    except Exception as error:
        logging.error(f"{error}")
        return None
    
def get_auth_id(user_email: str)-> int|bool:
    query = f"""
    SELECT id FROM {SIGNUP_TABLE} WHERE email = %s
    """    
    try:
        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute(query, (user_email,))
        result = cursor.fetchone()
        if not result:
            return None
        return result[0]
    except Exception as err:
        logging.error(err)
        return False
        
# Updating password corresponding
def update_password_sql(new_password: str, email: str) -> bool:
    try:
        query = f"""
                UPDATE {SIGNUP_TABLE} 
                set password = %s
                where email = %s
                """    
        # Hashing Password        
        hashed_password = hash_password(new_password)       
        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute(query, (hashed_password, email,))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as error:
        logging.error(f"{error}") 
        return False  
    
# This function updates date and time in sign up table if user email exists
def update_user_data(values: tuple)-> bool:  
    try:
        date_time, first_name, last_name, number, password, verify, user_role, email = values
        param = (date_time, first_name, last_name, number, password, verify, user_role, email)
        query = f"""
                UPDATE {SIGNUP_TABLE}
                SET date_time = %s, first_name = %s, last_name = %s, 
                number = %s, password = %s, verify = %s, user_role = %s
                WHERE email = %s;
            """    

        connection = db_connection()             
        cursor = connection.cursor()
        cursor.execute(query, param)
        connection.commit()
        cursor.close()     
        connection.close()    
        return True
    except Exception as err:
        logging.error(err)
        return False
    
# This function is responsible for returning a query which fetches user's role
def get_role_query()-> str:
    query = f"""
            SELECT user_role FROM {SIGNUP_TABLE} WHERE email = %s
        """    
    return query  


# This function is responsible for creating table for Vehicle pricing 
def create_pricing_table()-> str:
    query = f"""
            CREATE TABLE {VEHICLE_PRICING}
            (id SERIAL PRIMARY KEY, 
            vehicle_name VARCHAR, 
            code VARCHAR, 
            price_per_km float);
            """
    return query   


# This function is responsible for returning a query which insert vehicle price 
def insert_price_query()-> str:
    query = f"""
            INSERT INTO {VEHICLE_PRICING} (vehicle_name, code, price_per_km)
            VALUES (%s, %s, %s);
            """
    return query      

def fetch_price_query()-> str:
    query = f"""
            SELECT vehicle_name, code, price_per_km FROM {VEHICLE_PRICING}
            """
    return query        


def get_price_query()-> str:
    query = f"""
            SELECT price_per_km FROM 
            {VEHICLE_PRICING} 
            WHERE code = %s
            """
    return query        


def ride_history_query()-> str:
    query = f"""
            select date, time, pickup_address, drop_address,
            distance, vehicle_code, ride_fair, payment_status 
            FROM {CAB_BOOKING_TABLE} where auth_id = %s
            """
    return query   

def get_vehicle_name()-> str:
    query = f"""
            SELECT vehicle_name FROM {VEHICLE_PRICING} WHERE code = %s
            """     
    return query        