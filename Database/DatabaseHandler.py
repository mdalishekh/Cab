# This module is specially made for performing database related tasks
# Importing some useful Packages to be used in database related tasks
from Configuration.config import *
from Configuration.sqlQuery import *
from Database.JWT import *
from Database.LoginVerifier import *
from collections import defaultdict
import json

class DatabaseHandle:
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
                    token = jwt_encoder.encode_for_minutes({"email" : email}, 5) # Token is valid for only 5 minutes
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
        
    def cab_booking_insert(json_data: dict, user_email: str):
        connection = db_connection()
        cursor = connection.cursor()
        # Booking details to be inserted in Database
        pickup_address: str = json_data.get("pickupAddress")
        drop_address: str = json_data.get("dropAddress")
        pickup_coordinates: list[float, float] = json_data.get("pickupCoordinates")
        drop_coordinates: list[float, float] = json_data.get("dropCoordinates")
        booking_date: str = json_data.get("date")
        booking_time: str = json_data.get("time")
        distance: int = json_data.get("distance")
        vehicle_code = json_data.get("vehicleCode")
        
        # Getting the current default price per KM
        cursor.execute(get_price_query(), (vehicle_code,))
        default_price:int  = cursor.fetchone()[0]
        # Calculating the total price of the ride
        ride_fair: float = float(default_price * distance / 1000)
        ride_fair = max(ride_fair, default_price)
        auth_id: int = get_auth_id(user_email)
        if not auth_id or auth_id is None:
            return False
        values = (booking_date, booking_time, auth_id, pickup_address, 
                  drop_address, distance, pickup_coordinates,
                  drop_coordinates, vehicle_code,  ride_fair, True)
        # Inserting all details In Database
        if not is_table_exist(CAB_BOOKING_TABLE):
            try:
                logging.info("Cab booking table doesn't exist")
                logging.info("Creating Cab booking table")
                cursor.execute(booking_create_query())
            except:
                logging.error(f"Error in creating table {CAB_BOOKING_TABLE}")
        try:        
            cursor.execute(booking_insert_query(), values)
            connection.commit()
            logging.info("Cab booking data inserted into database")
            return True
        except Exception as err:
            logging.error(err)
            return False
        finally:
            cursor.close()
            connection.close()
            
    
    def get_ride_history(user_email: str)-> tuple[bool, dict|str]:
        """This function will provide ride history to users

        Args
        ----
            user_email (str): Takes email as parameter , to identify which is requesting for 
            for ride history

        Returns
        -------
            tuple[bool, dict|str]: returns boolean ans a dictionary with ride history
        """
        connection = db_connection()
        cursor = connection.cursor()
        auth_id: int = get_auth_id(user_email)
        if not auth_id or auth_id is None:
            logging.error(f"User not exist : {user_email}")
            return False, "User not exist"
        try:
            cursor.execute(ride_history_query(), (auth_id,))
            ride_history_data = cursor.fetchall()
            keys = [
                "date",
                "time",
                "pickupAddress",
                "dropAddress",
                "distance",
                "vehicleName",
                "rideFair",
                "paymentStatus"
            ]    
            ride_history_dict = {"rideHistory": []}
    
            for row in ride_history_data:
                # Convert the row into a dictionary
                record = dict(zip(keys, row))
                # Fetch vehicle name using the vehicle code
                vehicle_code = record["vehicleName"]  # Fetch the vehicle code (currently stored here)
                cursor.execute(get_vehicle_name(), (vehicle_code,))  # Query to get the vehicle name
                vehicle_name = cursor.fetchone()  # Fetch the result
                # Replace the vehicle code with the vehicle name
                if vehicle_name:
                    record["vehicleName"] = vehicle_name[0]  # Assuming the query returns a single value
                # Add the updated record to the ride history list
                ride_history_dict["rideHistory"].append(record)
            
            return True, ride_history_dict 
        except Exception as err:
            logging.error(err)
            return False, "No ride history found"   
                    
            
class PriceAction:
    """This class is for price related task from database
    """
    
    def default_fair_price()-> dict:
        """This method is for fetching price from database
        
        Args
        ----
            None
        
        Returns
        -------
            dict | None 
        """
        try:
            connection = db_connection()
            cursor = connection.cursor()
            cursor.execute(fetch_price_query())
            rows = cursor.fetchall()
            # Group data into the required JSON structure
            vehicle_data = defaultdict(list)
            for row in rows:
                vehicle_name, code, price_per_km = row
                vehicle_type = code[4:].upper()
                # Add the vehicle data to the corresponding category
                vehicle_data[vehicle_type].append({
                    "vehicleName": vehicle_name,
                    "vehicleCode": code,
                    "pricePerKM": price_per_km
                })
                
            # Convert defaultdict to a regular dict
            vehicle_data = dict(vehicle_data)
            # Return the JSON representation
            return vehicle_data
        except Exception as err:
            logging.error(f"{err}")
            return None
     
     
# This class is solely made to perform Admin task only     
class AdminAction:
    """
    This class is responsible for perform Database tasks
    only for `ADMIN ONLY`
    """         
    def insert_price(json_data: dict)-> tuple[bool, str]:
        """`ADMIN ONLY`
        This function will insert
        price in database table
        
        Args
        ----
            values (tuple): Values to be inserted into database

        Returns
        --------
            bool: True/False based on success
        """
        
        vehicle_name: str = json_data.get("vehicleName")
        vehicle_code: str = json_data.get("vehicleCode")
        price_per_km: float = json_data.get("pricePerKm")
        # Checking if price is float or not 
        if not isinstance(price_per_km, float):
            price_per_km: float = float(price_per_km)
        
        try:
            connection = db_connection()
            cursor = connection.cursor()
            if not is_table_exist(VEHICLE_PRICING):
                logging.info("Creating Vehicle pricing table")
                cursor.execute(create_pricing_table())
                logging.info("Vehicle pricing table has been created")
            try:
                cursor.execute(insert_price_query(), (vehicle_name, vehicle_code, price_per_km,))
                logging.info("Vehicle fiar price inserted")
            except Exception as er:
                logging.error(er)
            connection.commit()
            cursor.close()
            connection.close()
            return True, "Price added in Vehicle pricing table"
        except Exception as err:
            logging.error(f"{err}")
            return False, str(err)
        