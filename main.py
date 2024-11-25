# Importing some useful Packages to be used in this project 
from fastapi import FastAPI, Request, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from Configuration.config import *
from Configuration.sqlQuery import *
from Database.DatabaseHandler import *
from Database.LoginAndOtpVerifier import *
from Emails.MailSender import *
from Database.JWT import *
from Cron.cron import cron_scheduler

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

@app.get('/test')
def test_api():
    return {"status" : "Server is active"}

# Rest API for user account verification
@app.get("/api/v1/gocab/auth/signup/verify/token")
async def verify_signup_token(token: str = Form(...)):
    decoder = JwtDecoder
    status, result = decoder.decode_jwt(token)
    try:
        user_email = result.get("email")
    except:
        pass
    if status:
        set_verify_true(user_email)
        return JSONResponse({
                            "status" : True,
                            "message" : "You have been registerd",
                            },status_code= 200)
    # This is for negative scenario    
    return JSONResponse({
                        "result" : result
                        }, status_code= 401)    

# Rest API for user Sign up  
@app.post("/api/v1/gocab/auth/signup")
async def sign_up_api(request: Request) -> dict:
    # Getting the data from the request body
    logging.info("Starting API")
    json_data = await request.json()
    first_name = json_data.get("firstName")
    email = json_data.get("email")
    database = DatabaseHandler
    db_status, message = database.insert_signup_detail(json_data)
    if db_status:
        logging.info("Sign up details inserted in Database")
        jwt_encoder = JwtEncoder
        token = jwt_encoder.encode_for_minutes({"email" : email}, 5)
        token_url = f"http://localhost:3000/verify/token/{token}"
        email_status = account_verify_sender(email, first_name, token_url)
        if email_status:
            logging.info("Account verification email sent")
        else:
            message: str = "Email not sent"    
        # This response will be sent while True scenario will come    
        return JSONResponse({
                            "status" : True ,
                            "message" :"Account verification email sent",
                            "token" :token
                            }, status_code= 200)
    # This response will be sent while false scenario will come    
    return JSONResponse({
                        "status" : False ,
                        "message" :message
                        }, status_code= 200)


# This Rest APi for Login User with user credential
@app.post('/api/v1/gocab/auth/login')
async def login_api(request: Request) -> dict:
    try:
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