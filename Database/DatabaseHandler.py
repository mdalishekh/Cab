# This module is specially made for performing database related tasks
# Importing some useful Packages to be used in database related tasks
from Configuration.config import *
from Configuration.sqlQuery import *
from Database.JWT import *
from Database.LoginVerifier import *

class DatabaseHandler:
    """
    Class for database related operations.
    """
    # Insert Registation details.
    def insert_signup_detail(json_data: dict) -> tuple[bool, str]:
        """
        Extract Signup data from Json and inserts into `User_credential` table.
        
        Args
        ----- 
            (dict) :  Json data containing user details.
        
        Returns
        -------
            (bool)
        """
        connection = db_connection()
        cursor = connection.cursor() 
        try:
            
            # Extracting user details from Json
            first_name = json_data.get("firstName")
            last_name = json_data.get("lastName")
            number = json_data.get("phoneNumber")
            email = json_data.get("email")
            raw_password = json_data.get("password") 
            # Hashing password by bcrypt
            hashed_password = str(hash_password(raw_password))
            date, time = date_time()
            date_with_time = f"{date} - {time}"
            # Creating Sign Up table if not exist
            if not is_table_exist(SIGNUP_TABLE):
                logging.info("Sign up table doesn't exist")
                try:
                    cursor.execute(signup_create_query())
                    logging.info("Sign up table has been created")
                except Exception as e:
                    logging.error(f"An error occurred while creating table: {e}")    
            else:
                logging.info("Table already exist")
            
        # Verifying if user exist and verified or not 
            if is_user_exist(email):
                logging.info(f"User email exist in database : {email}")
                if is_user_verified(email):
                    logging.info(f"User already verified : {email}")
                    return False, "User already registered"
                else:
                    logging.info(f"User is not verified : {email}")
                    values = (date_with_time, first_name, last_name, number, hashed_password, False, "USER",  email,)
                    update_user_data(values)
                    return True, "Data inserted in database"
            else:
                logging.info(f"User not exist : {email}")  
            logging.info(f"Inserting data for new user : {email}")    
            values = (date_with_time, email, first_name, last_name, number, hashed_password, False, "USER")
            # Inserting user details into `User_credential` table
            cursor.execute( signup_insert_query(), values)
            connection.commit()
            cursor.close()
            return True, "Data inserted successfully"
        except Exception as error:
            logging.error(f"error caused : {error}")
            return False, None
        
    # This fucntion is for Login verification
    def login_verification(json_data: dict) -> tuple[bool, str|None, str|None]:
        """
        This funcion is responsivle for login verification

        Args
        ----
            (dict) : Takes json values as disctionary contains user credentials.

        Returns
        -------
            tuple[bool, str|None, str|None]: If password verified then return with JWT.
        """
        
        try:
            email = json_data.get("email")
            password = json_data.get("password")
            # Making database connection 
            connection = db_connection()
            if is_user_exist(email):
                logging.info(f"User is registered : {email}")
                if is_user_verified(email):
                    logging.info(f"User is verified : {email}")
                else:
                    logging.error(f"User not verified : {email}")
                    return False, "User not verified", None
            else:
                logging.error(f"User not registered : {email}")
                return False, "User not registered", None
            # Making database cursor and executing furthur task
            cursor = connection.cursor()
            cursor.execute(fetch_password_query(), (email,))
            fetched_password = "".join(cursor.fetchone())
            # Checking if pasword matched 
            is_password_correct = verify_hashed_password(password, bytes(fetched_password.encode('utf-8')))
            # Checking if password is correct or not
            if is_password_correct:
                logging.info(f"Hashed Password matched")
                try: 
                    jwt_encoder = JwtEncoder
                    token = jwt_encoder.encode_for_minutes({"email" : email}, 5)
                except Exception as error:
                    logging.error(f"{error}")
                cursor.close()
                connection.close()
                return True, "Password matched", token
            # If passowrd didn't matched
            logging.error(f"Password didn't matched")
            cursor.close()
            connection.close()
            return False, "Invalid credentials", None
        except Exception as error:
            logging.error(f"{error}")    
            return False, None, None