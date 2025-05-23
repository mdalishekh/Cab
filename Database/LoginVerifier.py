# This module is specially made for verify OTP and verify if the user is Logged in or not
from Configuration.config import *
from Configuration.sqlQuery import *
import bcrypt


# This function encrypt password
def hash_password(plain_password: str) -> bytes:
    """
    Hash a plain text password using bcrypt algorithm.

    This function takes a plain password string, applies bcrypt hashing with a secret key 
    retrieved from environment variables, and returns the hashed password as a UTF-8 string.

    Parameters
    ----------
    plain_password : str
        The plain text password to be hashed.

    Returns
    -------
    bytes or None
        The bcrypt-hashed password as a UTF-8 encoded byte string if successful; 
        returns None if an error occurs during hashing.
    """

    try:
        BCRYPT_KEY = os.getenv("BCRYPT_KEY")
        byte_text = bcrypt.hashpw(plain_password.encode('utf-8'), BCRYPT_KEY.encode('utf-8'))
        encrypted_password = byte_text.decode('utf-8')
        return encrypted_password
    except Exception as err:
        logging.error(err)
        return None

# This function decrypt password and matches it , and returns bool
def verify_hashed_password(plain_password: str, hashed_password: bytes) -> bool:
    # Check if the hashed password matches the provided password
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)
    except Exception as err:
        logging.error(err)
        return None
