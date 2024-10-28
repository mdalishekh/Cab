# This module is intentionally made for returning all SQL queries.
from Configuration.config import *

# Setting a table name to be created in run time 
REGISTRAION_TABLE_NAME  = 'registration_details'
OTP_TABLE_NAME = 'otp_verification'
BOOKING_TABLE_NAME = 'bookings'



# Creating a table in Postgres SQL for Registraion
def registration_create_query():
    query = f'''
            CREATE TABLE {REGISTRAION_TABLE_NAME} (
                ID SERIAL PRIMARY KEY,
                user_email VARCHAR,         
                first_name VARCHAR,         
                last_name VARCHAR,          
                phone_number VARCHAR,        
                user_password VARCHAR,      
                registration_date DATE,     
                registration_time TIME      
            );
            '''
    return query


# This function is responsible to insert user's registration data into database            
def registration_insert_query():
    query = f'''
            INSERT INTO {REGISTRAION_TABLE_NAME} (
                user_email, 
                first_name, 
                last_name, 
                phone_number, 
                user_password, 
                registration_date, 
                registration_time
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s);
            '''        
    return query     


#  Creating a table in Postgres SQL for OTP verification    
def otp_verification_create_query():
    query = f'''
             CREATE TABLE {OTP_TABLE_NAME} (
                ID SERIAL PRIMARY KEY,
                user_email VARCHAR,
                OTP VARCHAR,
                is_valid BOOLEAN,
                otp_date DATE,
                otp_time TIME,
                can_change_password BOOLEAN
            );
            '''       
    return query


# This function is responsible to insert user's registration OTP data into database
def otp_insert_query():
    query = f'''
            INSERT INTO {OTP_TABLE_NAME} (user_email, OTP, is_valid, otp_date, otp_time, can_change_password)
            VALUES (%s, %s, %s, %s, %s, %s);
             '''
    return query


# This function is responsible to return Booking table create query
def booking_create_query():
    query = f"""
            CREATE TABLE {BOOKING_TABLE_NAME} (
            id SERIAL PRIMARY KEY,
            user_email VARCHAR,
            pickup_location VARCHAR,
            drop_location VARCHAR,
            booking_date DATE,
            booking_time TIME
            );
            """
    return query


# This function is responsible to create Booking table
def booking_create_table():
    try:
        cursor = DB_CONNECTION.cursor()
        cursor.execute(booking_create_query())
    except:
        return None


# This function is responsible to return Booking table insert query
def booking_insert_query():
    query = f"""
            INSERT INTO {BOOKING_TABLE_NAME} 
            (user_email, pickup_location, drop_location, booking_date, booking_time)
            VALUES (%s, %s, %s, %s, %s);
            """
    return query


# OTP validator fetch query
def fetch_otp_query():
    query = f"""
            SELECT otp, is_valid 
            FROM {OTP_TABLE_NAME} WHERE 
            user_email = %s
            """
    return query


# This function is responsible for returning a query to update OTP
def update_otp_query():
    otp_update_query = f"""
                    UPDATE {OTP_TABLE_NAME}
                    SET otp = %s, is_valid = true,
                    otp_date = %s, otp_time = %s
                    WHERE user_email = %s;
                    """
    return  otp_update_query


# This function is resposible for returning a query to check the table exists or not
def is_table_exist_query(table_name):
    query = f"""
                SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_name = '{table_name}'
            );
            """ 
    return query        


# This function is resposible for check the table exists or not 
def is_table_exist(table_name):
    try:
        pg_cursor = DB_CONNECTION.cursor()
        pg_cursor.execute(is_table_exist_query(table_name), (table_name,))
        exists = pg_cursor.fetchone()[0]
        pg_cursor.close()
        return exists
    except Exception as error:
        logging.error(f"ERROR OCCURED WHILE CHECKING {table_name} EXISTANCE: " f"{error}")
        return False


def is_user_exist(user_email, table_name):
    # Connecting with Database 
    try:
        cursor = DB_CONNECTION.cursor()
        exists = is_table_exist(table_name)
        if exists:
            email_exist_query = f"""
                    SELECT EXISTS (
                    SELECT 1 
                    FROM {table_name}
                    WHERE user_email = %s
                    );
                    """
            cursor.execute(email_exist_query, (user_email,))
            email_exist = cursor.fetchone()[0]
            return email_exist
        return False
    except Exception as error:
        logging.error(f"Error occurred while checking user existence: {error}")
        return False
    
    
def get_first_name(user_email):
    cursor = DB_CONNECTION.cursor()
    if is_user_exist(user_email, REGISTRAION_TABLE_NAME):
        query = f"""
                SELECT first_name FROM 
                {REGISTRAION_TABLE_NAME} WHERE user_email = %s
                """
        cursor.execute(query, (user_email,))        
        first_name = cursor.fetchone()[0]
        return first_name
    return None   


# OTP devalidator query
def otp_devalid_query():
    query = f'''
                UPDATE {OTP_TABLE_NAME}
                SET is_valid = false
                WHERE user_email = %s;
                '''
    return query


# Update password query
def update_password_query():
    query = f'''
            UPDATE {REGISTRAION_TABLE_NAME}
            SET user_password = %s,
            registration_date = %s,
            registration_time = %s
            WHERE user_email = %s
            '''
    return query             


# Fetch password query
def fetch_password_query():
    query = f"""
            SELECT user_password 
            FROM {REGISTRAION_TABLE_NAME} 
            WHERE user_email = %s
            """
    return query


# This if user is eligible to update their password
def is_user_eligible(user_email):
    cursor = DB_CONNECTION.cursor()
    query = f"""
            SELECT can_change_password 
            FROM {OTP_TABLE_NAME} 
            WHERE user_email = %s
            """
    cursor.execute(query, (user_email,))        
    is_user_eligible = cursor.fetchone()[0]
    return is_user_eligible             
                   
                   
# This query will allow and deny the permission of changing password with / without OTP
def can_change_allow_query():
    query = f"""
            UPDATE {OTP_TABLE_NAME}
            SET otp_date = %s, 
            otp_time = %s, can_change_password = %s
            WHERE user_email = %s;
            """
    return query
