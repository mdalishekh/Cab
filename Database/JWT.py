"""
This Module handle entire `JWT` operations.
"""

import jwt  
from datetime import datetime, timedelta, timezone
from Configuration.config import *

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
            return payload
        except jwt.ExpiredSignatureError as error:
            logging.error(f"{error}")    
            return jwt.ExpiredSignatureError
        except jwt.InvalidTokenError as error:
            logging.error(f"{error}")
            return jwt.InvalidTokenError
        
        