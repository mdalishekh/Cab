# This module is specially made for performing database related tasks
# Importing some useful Packages to be used in database related tasks
from Configuration.config import *
from Configuration.sqlQuery import *
from Database.JWT import *

class DatabaseHandler:
    """
    Class for database related operations.
    """
    # Insert Registation details.
    def insert_signup_detail(json_data: dict) -> bool:
        """
        Extract Signup data from Json and inserts into `User_credential` table.
        
        Args:
            >>> 
        json_data (dict): Json data containing user details.
        
        Returns:
        >>> bool
        """
        try:
            
            # Extracting user details from Json
            first_name = json_data.get("firstName")
            last_name = json_data.get("lastName")
            number = json_data.get("phoneNumber")
            email = json_data.get("email")
            raw_password = json_data.get("password")
            # Encoding Password in JWT
            encoder = JwtEncoder
            encoded_password = encoder.encode_no_expire({"password" : raw_password})
            date, time = date_time()
            date_with_time = f"{date} - {time}"
            values = (date_with_time, email, first_name, last_name, number, encoded_password, False, "USER")
            # Checking if connection already exist or not 
            cursor = DB_CONNECTION.cursor()    
            if not is_table_exist(SIGNUP_TABLE):
                logging.info("Sign up table doesn't exist")
                try:
                    cursor.execute(signup_create_query())
                    logging.info("Sign up table has been created")
                except Exception as e:
                    logging.error(f"An error occurred while creating table: {e}")    
            else:
                logging.info("Table already exist")
            # Inserting user details into `User_credential` table
            cursor.execute( signup_insert_query(), values)
            DB_CONNECTION.commit()
            cursor.close()
            return True
        except Exception as error:
            logging.error(f"{error}")
            return False