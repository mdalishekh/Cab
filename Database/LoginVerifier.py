# This module is specially made for verify OTP and verify if the user is Logged in or not
from Configuration.config import *
from Configuration.sqlQuery import *
import bcrypt


# This function encrypt password
def hash_password(plain_password: str) -> bytes:
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
