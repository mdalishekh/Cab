"""
This Module handle entire `JWT` operations.
"""

import jwt  
from datetime import datetime, timedelta, timezone
from Configuration.config import *
from cryptography.fernet import Fernet


class JwtEncoder:
    """
    This class contains all types of `JWT` encoding operations.
    """
    # This function will encode any parameter with No expiration.
    def encode_no_expire(json_data: dict) -> str:
        """
        This function will encode any Dictionary in `JWT` without any expiration.
        
        Args
        ----
            >>>
        json_data (dict): Takes JSON/dict parameter to encode.
        
        Returns
        -------
            >>>
        (str) : JWT token
        """
        # Encoding json data into JWT
        token = jwt.encode(json_data, JWT_SECRET, ALGORITHM)
        return token
    
    
    # This function will encode any parameter with No expiration.
    def encode_for_minutes(json_data: dict, expire_period: int) -> str:
        """
        This function will encode any Dictionary in `JWT` for a limited time.
        
        Args
        ----
            >>>
        json_data (dict): Takes JSON/dict parameter to encode.
        expire_period (int): Takes minute value to expire within minutes as int, Like 1, 2, or 3.
        
        Returns
        -------
            >>>
        (str) : JWT token
        """
        json_data.update({
        'iat': datetime.now(timezone.utc),  # Issued at current time in UTC
        'exp': datetime.now(timezone.utc) + timedelta(minutes=expire_period)  # Expiration time
        })
        # Encoding json data into JWT
        token = jwt.encode(json_data, JWT_SECRET, ALGORITHM)
        return token
    
    
        
        
class JwtDecoder:
    """
    This class contains all types of `JWT` decoding operations.
    """        
    # This function will decode any JWT token and return actual JSON data.
    def decode_jwt(token: str) -> dict | bool:
        """
        This function will decode all `JWT` and return actual JSON.
        
        Args
        ----
            >>>
        token (str) : Takes actual JWT for decoding.
        
        Returns
        -------
            >>>
        dict | bool : If Signature or token is Valid then dict, otherwise bool.
        """
        try:
            payload: dict = jwt.decode(token, JWT_SECRET, ALGORITHM)
            return True, payload
        except jwt.ExpiredSignatureError as signature_expire:
            logging.error(f"{signature_expire}")    
            return False, "Session has expired"
        except jwt.InvalidTokenError as invalid_token:
            logging.error(f"{invalid_token}")
            return False, "Invalid Token"
        

class CryptoGraphy:
    """
    This class encrypt and decrypt text or password.
    
    Functions
    ---------
    encrypt_text(text: str) -> str
    decrypt_text(text: str) -> str
    """
    
    def __init__(self, key) -> None:
        self.key = key
     
    def encrypt_text(self, text: str) -> bytes:
        """
        This function will encrypt text or password and will return a bytes code.
        
        Args
        ----
            str : `text` Text or password to be encrypted.
            
        Returns
        -------
            bytes : Encrypted bytes code.
        """
        cipher_suite = Fernet(self.key)
        encoded_text = cipher_suite.encrypt(text.encode('utf-8'))
        return encoded_text
    
    def decrypt_byte(self, encoded_text: bytes) -> str:
        """
        This function will decrypt bytes code and will return a actual str.
        
        Args
        ----
            bytes : `encoded_text` Encrypted bytes code.
            
        Returns
        -------
            str : Actual str.
        """
        cipher_suite = Fernet(self.key)
        decoded_text = cipher_suite.decrypt(encoded_text)
        return decoded_text.decode('utf-8')