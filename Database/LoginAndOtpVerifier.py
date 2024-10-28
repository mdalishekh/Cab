# This module is specially made for verify OTP and verify if the user is Logged in or not
from Configuration.config import *
from Configuration.sqlQuery import *


# This function is responsible for validate OTP from database
def otp_validator(user_email, OTP):
    cursor = DB_CONNECTION.cursor()
    cursor.execute(fetch_otp_query(), (user_email,))
    result = cursor.fetchone()
    fetched_otp, is_valid = result
    cursor.close()
    if is_valid:
        if OTP == int(fetched_otp):
            logging.info("OTP has been verified")
            return True, "You have been registered"
        logging.error(f"User '{user_email}' entered an incorrect OTP")
        return False, "Incorrect OTP"
    logging.error(f"OTP has been expired for user '{user_email}' ")
    return False, "OTP is expired"


# This function is responsible to authenticate users
def authenticate_user(user_email, user_password):
    cursor = DB_CONNECTION.cursor()
    # Checking if email entered by user is valid or not
    logging.info(f"Checking if {user_email} exist or not")
    # If email entered by user exists now authenticate
    exists = is_user_exist(user_email, REGISTRAION_TABLE_NAME)    
    if exists:
        logging.info(f"A user with email {user_email} exists")
        cursor.execute(fetch_password_query(), (user_email,))
        fetched_password = cursor.fetchone()[0]
        cursor.close()
        if fetched_password == user_password:
            message = f"Login successfully"
            logging.info(f"User '{user_email}' has been authenticated")
            return True, message
        message = "Incorrect password"
        logging.error(message)    
        return False, "Incorrect password"
    message = f"User '{user_email}' not exist"
    logging.error(message)
    return False, "User not exist"


# This function is responsible for De-validate OTP in Database 
def otp_devalidator(user_email):
    try:
        # Trying to connect with Database 
        cursor  = DB_CONNECTION.cursor()
        cursor.execute(otp_devalid_query(), (user_email,))
        DB_CONNECTION.commit()
        cursor.close()         
        logging.info("OTP HAS BEEN DE-VALIDATED or EXPIRED")
        return True
    except Exception as error:
        logging.error(f"error occurred while devalidating OTP : {error}")