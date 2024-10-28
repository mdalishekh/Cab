# Importing some useful Packages to be used in this project 
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from Configuration.config import *
from Configuration.sqlQuery import *
from Database.DatabaseHandler import *
from Database.LoginAndOtpVerifier import *
from Emails.MailSender import *
from Cron.cron import cron_scheduler
import random

# Initiating an instance for FastAPI 
app = FastAPI()

# Define the origins you want to allow
origins = [
    "http://127.0.0.1:5500",  # Your frontend URL
    "http://localhost:5500",
    "http://127.0.0.1:5501",
    "http://127.0.0.1:5500/",
    "https://gocab.netlify.app",
    "https://gocab.netlify.app/",
    # You can add more origins here if needed
]

# Add the CORS middleware to the FastAPI application
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Origins allowed to make requests
    allow_credentials=True,  # Allow cookies to be sent with requests
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Creating a route for keeping server active
@app.get('/')
def cron_expression():
    cron_scheduler()
    return JSONResponse({"response": "Our Application / Server is active"})

# Creating a route for testing our REST API with GET method
@app.get('/test-api')
def test_api():
    logging.info("Our Application / Server is active")
    return JSONResponse({"response": "Our Application / Server is active"})
   
# 1.Creating a route for sending OTP to users via e-mail
@app.post('/api/v1/go-cab/send-otp')
async def send_otp_api(request:Request):
    try:
        logging.info("---------------------------------------------------------")
        logging.info("OTP SENDING HAS BEEN INITIATED")
        json_data = await request.json()
        user_email = json_data.get('userEmail')
        user_first_name = json_data.get('firstName')
        OTP = random.randint(100000, 999999)
        # Inserting OTP details in Database
        is_done, message = insert_otp_details(user_email, OTP)
        # Sending OTP to user email if user is not registered with same email
        if is_done:
            status = send_otp_by_mail(user_email, user_first_name, OTP)
            logging.info(f"Generated OTP for {user_email} is : {OTP}")
            # If OTP is successfully sent to user email
            if status:
                logging.info(f"OTP HAS BEEN SENT TO {user_email}")
                response = {"status": status,"message" : f"{message}", "OTP" : OTP}
                return  JSONResponse(response, status_code=200)
            return JSONResponse({"status" : status, "message" : f"Failed to send OTP"}, status_code=200)
        return JSONResponse({"status" : is_done, "message" : message}, status_code=200)
    except Exception as error:
        logging.error(f"ERROR OCCURED WHILE SENDING OTP TO {user_email}")
        return JSONResponse({"error occured while sending otp" : error}, status_code= 500)
    
    
# 2. Creating route for sending registration success to users via e-mail     
@app.post('/api/v1/go-cab/otp-verification')
async def otp_verification_api(request:Request):
    try:
        logging.info("---------------------------------------------------------")
        logging.info("OTP VERIFICATION HAS BEEN INITIATED")
        # Getting JSON data  
        json_data = await request.json()
        user_email = json_data.get('registrationDetails').get('userEmail')
        user_first_name = json_data.get('registrationDetails').get('firstName')
        OTP = int(json_data.get('OTP'))        
        
        # validating OTP if it's correct or not
        is_otp_valid , message = otp_validator(user_email, OTP)
        if is_otp_valid:
            # If OTP verification is success
            logging.info(f"User {user_email} has been verified")
            # If OTP verified then insert user details in database
            insert_registration_details(json_data)
            # Now sending confirmation email to user , that user have been registered with us
            status = registration_success_mail(user_email, user_first_name)
            # Now De-validating / Expiring OTP for user 
            otp_devalidator(user_email)
            # If OTP is correct and confirmation Email sent to user
            if status:
                logging.info(f"CONFIRMATION E-MAIL HAS BEEN SENT TO THE {user_email}")
                response = {"status": status,"message" : message}
                return  JSONResponse(response)
            # If OTP is correct but confirmation E-mail not sent to user
            return JSONResponse({"status" : status, "message" : f"Failed to register"}, status_code=200)
        logging.info("OTP validation has failed")
        return JSONResponse({"status" : False, "message" : message})
        
    except Exception as error:
        logging.error(f"ERROR OCCURED WHILE SENDING CONFIRMATION E-MAIL : {user_email}")
        return JSONResponse({"error occured while sending confirmation e-mail" : error}, status_code= 500)
                
    
# 3. Creating a route for User Login
@app.post('/api/v1/go-cab/authenticate')
async def user_login_api(request:Request):
    try:
        logging.info("---------------------------------------------------------")
        logging.info("USER AUTHENTICATION HAS BEEN INITIATED")
        json_data = await request.json()
        user_email = json_data.get('userEmail')
        password = json_data.get('password')
        status, message = authenticate_user(user_email, password)
        if status:
            logging.info("USER AUTHENTICATION HAS BEEN COMPLETED")
            first_name = get_first_name(user_email)
            response = {"status" : status, "userEmail" : user_email, "firstName" : first_name, "message" : message}
            return JSONResponse(response)
        return JSONResponse({"status" : status, "userEmail" : user_email, "message" : message}, status_code= 200)
    except Exception as error:    
        logging.error(f"ERROR OCCURED WHILE AUTHENTICATING USER : {error}")
        return JSONResponse({"error occured while authenticating user" : error}, status_code= 500)   
    
    
# 4. Creating a route for Forgot password request email verify
@app.post('/api/v1/go-cab/verify-email')
async def forgot_email_verify_api(request:Request):
    try:
        logging.info("---------------------------------------------------------")
        logging.info("EMAIL VERIFICATION FOR PASSWORD CHANGE HAS BEEN INITIATED")
        json_data = await request.json()
        user_email = json_data.get("userEmail")
        logging.info(f"Verifying email regsitered or not {user_email}")
        # Checking if the user exist or not , If exist then getting True with their First name
        is_exist = is_user_exist(user_email, REGISTRAION_TABLE_NAME)
        if is_exist:
            logging.info(f"User with email {user_email} exist")
            fisrt_name = get_first_name(user_email)
            OTP = random.randint(100000, 999999)
            logging.info(f"Generated OTP for password change : {OTP}")
            db_status, message = insert_forgot_otp(user_email, OTP)
            status = forgot_password_otp_send(user_email, fisrt_name, OTP)
            if status and db_status:
                logging.info(f"OTP has been sent to '{user_email}' ")
                return JSONResponse({"status" : status, "message" : message, "OTP" : OTP}, status_code=200)
            return JSONResponse({"status" : False, "message" : f"Failed to verify"},status_code=200)
        logging.error(f"No user exist with email = '{user_email}' ")
        return JSONResponse({"status" : False, "message" : f"User not exist"},status_code=200)
    except Exception as error:
        logging.error(f"ERROR OCCURED WHILE VERIFYING EMAIL : {error}")
        return JSONResponse({"error occured while verifying email" : error}, status_code= 500)


# 5. Creating a route for Forgot password request OTP verify
@app.post('/api/v1/go-cab/forgot-verify-otp')
async def forgot_otp_verify_api(request: Request):
    try:
        logging.info("---------------------------------------------------------")
        logging.info("OTP VERIFICATION FOR PASSWORD CHANGE HAS BEEN INITIATED")
        json_data = await request.json()
        user_email = json_data.get('userEmail')
        OTP = json_data.get('OTP')
        is_otp_valid , message = otp_validator(user_email, OTP)
        if is_otp_valid:
            logging.info("OTP verified successfully")
            logging.info(f"User '{user_email}' is now Authorized / Verified to change their password")
            otp_devalidator(user_email)
            logging.info("Now OTP has been De-Validated or Expired")
            # Making user eligible to change their password
            password_change_eligibility(user_email, True)
            return JSONResponse({"status" : True, "message" : "You have been verified"},status_code = 200)
        return JSONResponse({"status" : False, "message" : message},status_code = 200)
    except Exception as error:
        logging.error(f"ERROR OCCURED WHILE VERIFYING OTP : {error}")
        return JSONResponse({"error occured while verifying OTP" : error}, status_code= 500)
    
    
# 6. Creating a route for Forgot password request Update password
@app.post('/api/v1/go-cab/new-password')
async def forgot_otp_verify_api(request: Request):
    try:
        logging.info("---------------------------------------------------------")
        logging.info("CHANGING PASSWORD HAS BEEN INITIATED")
        json_data = await request.json()
        user_email = json_data.get('userEmail')
        new_password = json_data.get('newPassword')
        if is_user_eligible(user_email):
            logging.info("User is eligible to change their password")
            logging.info(f"Changing password for {user_email}")
            status, message = update_password(user_email, new_password)
            if status:
                password_change_eligibility( user_email, False) # Making user ineligible to change their password
                logging.info(F"PASSWORD CHANGED SUCCESSFULLY FOR '{user_email}' ")
                return JSONResponse({"status" : True, "message" : message}, status_code= 200)
            logging.error(f"Couldn't change password for {user_email}")
        logging.error(f"User '{user_email}' is not Authorized / Verified to change their password")    
        return JSONResponse({"status" : False, "message" : "Can't change password"}, status_code= 200)
    except Exception as error:
        logging.error(f"ERROR OCCURED WHILE CHANGING PASSWORD : {error}")
        return JSONResponse({"error occured while changing password" : error}, status_code= 500)
    
    
# 7. Creating a route for Inserting Booking data in database
@app.post('/api/v1/go-cab/book-ride')
async def insert_booking_api(request: Request):
    try:
        logging.info("---------------------------------------------------------")
        logging.info("CAB BOOKING HAS BEEN INITIATED")
        json_data = await request.json()
        status = insert_booking_details(json_data)
        if status:
            logging.info("CAB BOOKED SUCCESSFULLY")
            return JSONResponse({"status" : True, "message" : "You're cab is booked"})  
        return JSONResponse({"status" : False, "message" : "User not exist"})
    except Exception as error:
        logging.error(f"ERROR OCCURED WHILE INSERTING BOOKING DATA : {error}")
        return JSONResponse({"error occured while inserting booking data " : error}, status_code= 500)