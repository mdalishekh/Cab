# Importing some useful Packages to be used in this project 
from fastapi import FastAPI, Request, Form, Header, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from Cron.cron import cron_scheduler
from Emails.MailSender import *
from Database.DatabaseHandler import *
from Database.LoginVerifier import *
from Database.JWT import *
from Database.AuthConfig import *
from Configuration.UiRoutes import *
from Configuration.config import *
from Configuration.sqlQuery import *
from Configuration.ApiRoutes import *


# Initiating an instance for FastAPI 
app = FastAPI()

# Define the origins you want to allow
origins = [
    "http://127.0.0.1:5500",  # Your frontend URL
    "http://localhost:5500",
    "http://127.0.0.1:5501",
    "http://127.0.0.1:5500/",
    "https://go-cab-ten.vercel.app",
    "https://go-cab-ten.vercel.app/",
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

# Rest API for activate server
@app.get('/test')
def test_api():
    logging.info("-------------------------")
    logging.info("\tServer is active")
    logging.info("-------------------------")
    return {"status" : "Server is active"}


# Rest API for user Sign up  
@app.post(SIGNUP_API_URL)
async def sign_up_api(request: Request) -> dict:
    # Getting the data from the request body
    logging.info("Sign Up API initiated")
    json_data = await request.json()
    first_name = json_data.get("firstName")
    email = json_data.get("email")
    database = DatabaseHandler
    db_status, message = database.insert_signup_detail(json_data)
    # Checking if data is inserted in database or not
    if db_status: 
        logging.info("Sign up details inserted in Database")
        jwt_encoder = JwtEncoder
        token = jwt_encoder.encode_for_minutes({"email" : email}, 5)
        # Generating frontend url for account verification
        token_url = account_verify_url(token)
        email_status = signup_verify_sender(email, first_name, token_url)
        # Checking if email is sent or not
        if email_status:
            logging.info("Account verification email sent")
        else:
            message: str = "Email not sent"    
        # This response will be sent while True scenario will come    
        return JSONResponse({
                                "status" : True ,
                                "message" : "Account verification email sent",
                            }, status_code= 200)
    # This response will be sent while false scenario will come    
    return JSONResponse({
                            "status" : False ,
                            "message" : message
                        }, status_code= 401)


# Rest API for user account verification
@app.post(SIGNUP_VERIFY_TOKEN_API_URL)
async def verify_signup_token(token: str = Form(...)):
    decoder = JwtDecoder
    status, payload = decoder.decode_jwt(token)
    try:
        user_email = payload.get("email")
    except:
        logging.error(f"{payload} for user")
    if status:
        set_verify_true(user_email)
        return JSONResponse({
                                "status" : True,
                                "message" : "You have been registered",
                            },status_code= 200)
    # This response will be delivered when token is Invalid/Expired  
    return JSONResponse({
                            "status" : False,
                            "message" : payload
                        }, status_code= 401)    


# This Rest APi for Login User with user credential
@app.post(LOGIN_API_URL)
async def login_api(request: Request) -> dict:
    try:
        logging.info("Login API initiated")
        json_data = await request.json()
        database = DatabaseHandler
        status, message, token = database.login_verification(json_data)
        if status:
            logging.info(f"{message}")
            return JSONResponse({
                                    "status" : True ,
                                    "message" : message,
                                    "token" : token
                                }, status_code=200)
        else:
            logging.error(f"{message}")
            return JSONResponse({
                                    "status" : False ,
                                    "message" : message
                                }, status_code= 401)
    except Exception as error:
        logging.error(f"{error}")
        JSONResponse({"error occurred while login " : error}) 
        
        
# Rest API to get email for forget password
@app.post(FORGET_PASSWORD_API_URL)
async def email_forget_password_api(request: Request) -> dict:
    try:
        logging.info("Forget Password email API initiated")
        json_data = await request.json()
        email = json_data.get("email")
        if is_user_exist(email):
            logging.info("User found in database")
            if is_user_verified(email):
                logging.info("User is verified")
                jwt_encoder = JwtEncoder
                token = jwt_encoder.encode_for_minutes({"email": email}, 5)
                # Generating frontend url for forgot password email verification
                token_url = forgot_password_url(token)
                first_name = get_first_name(email)
                email_status = forgot_password_verify_sender(email, first_name, token_url)
                if email_status:
                    logging.info(f"Forget password verification Email sent to : {email}")
                    return JSONResponse({
                                            "status" : True,
                                            "message" : "Email sent successfully"
                                        }, status_code= 200)
                else:
                    logging.error(f"Email not sent to : {email}")
                    return JSONResponse({
                                            "status" : False,
                                            "message" : "Email not sent"
                                        }, status_code= 404)
            else:
                logging.info("User is not verified")
                # This response will be sent while user is not verified
                return JSONResponse({
                    "status" : False,
                    "message" : "User is not verified"
                }, status_code= 404)
        else:
            logging.info("User not found in database")
            return JSONResponse({
                                    "status" : False,
                                    "message" : "User not found"
                                }, status_code= 404)
    except Exception as error:
        logging.error(f"{error}")
        JSONResponse({"error occurred while getting email " : error})    
        
        
   
# Rest api for changing password 
@app.post(UPDATE_PASSWORD_API_URL)
async def change_password_api(request: Request) -> dict:
    try:
        logging.info("Changing password API initiated")
        json_data = await request.json()
        new_password = json_data.get("confirmPassword")
        token = json_data.get("token")
        jwt_decoder = JwtDecoder
        decode_status, decoded_str = jwt_decoder.decode_jwt(token)
        if decode_status:
            logging.info("Token is valid")
        else:
            logging.info(f"{decoded_str}")
            return JSONResponse({
                    "status": False, 
                    "message": decoded_str
                }, status_code= 401)
            
        email = decoded_str.get("email")
        update_status = update_password_sql(new_password, email)
        if update_status:
            logging.info("Password changed successfully")
            return JSONResponse({
                "status": True,
                "message": "Password changed successfully"
            })
        else:
            logging.error(f"Password not updated for user : {email}")
            return JSONResponse({
                                    "status" : False,
                                    "message" : "Password not updated"
                                })
    except Exception as error:
        logging.error(f"{error}")
        return JSONResponse({"error occurred while changing password " : error})
    
    

# Rest API for Price insertion in Database (Admin access only)
@app.post(PRICE_INSERTION_API_URL)
async def price_insertion(request: Request,
                        authorization: str = Header(...)
                        )-> dict:
    # Validate and extract the token
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header")
    token = authorization[len("Bearer "):]
    jwt_decoder = JwtDecoder
    status, payload = jwt_decoder.decode_jwt(token)
    if not status:
        return JSONResponse({
                            "status": False,
                            "message" : payload
                            }, status_code=401)
    # Extracting user email from JWT payload
    user_email = payload.get("email")  
    auth_security = AuthSecurityFilter
    if not auth_security.has_access(user_email, "ADMIN"):
        return JSONResponse({
                                "status" : False,
                                "message" : "You don't have sufficient permission to access this API."
                            }, status_code=401)
        
    # Parse JSON data from the request body
    try:
        json_data:dict = await request.json()
        # Inserting price into database
        admin_action = AdminAction
        status, message = admin_action.insert_price(json_data)
        if not status:
            return JSONResponse({
                                    "status" : False,
                                    "message" : message
                                }, status_code=500)
        return JSONResponse({
                                "status" : True,
                                "message" : message
                            }, status_code= 201)
    except Exception as e:
        raise HTTPException(status_code=400, detail= e)
    