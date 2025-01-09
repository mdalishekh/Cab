"""
    This module is responsible for verifying if the user have
    any specific access or not
"""

from configuration.config import *
from Database.DatabaseHandler import *

class AuthSecurityFilter:
    """
    This class is responsible for verifying if the user have any specific access or not
    """
    
    # Checks if user have ADMIN access or not    
    def has_access(user_email: str, role: str)-> bool:
        """This function checks if the user have ROLE access or not

        Args
        ----
            user_email (str): Provide user email to be verified

        Returns
        -------
            bool: If user has ROLE then TRUE, else FALSE
        """
        if not is_table_exist(SIGNUP_TABLE):
            return False
        if not is_user_exist(user_email):
            return False
        if not is_user_verified(user_email):
            return False
        try:
            connection = db_connection()
            cursor = connection.cursor()
            cursor.execute(get_role_query(), (user_email,))
            fetched_result: str = "".join(cursor.fetchone())
            if fetched_result.lower() == role.lower():
                cursor.close()     
                connection.close() 
                logging.info(f"User have {role.upper()} access :  {user_email}")
                return True
            cursor.close()     
            connection.close() 
            logging.error(f"User doesn't have {role.upper()} access : {user_email}")
            return False
        except Exception as err:
            logging.error(f"{err}")
            return False
            