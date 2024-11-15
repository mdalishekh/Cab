# Importing some useful Packages to be used in this project 
from fastapi import FastAPI, Request
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

@app.get("/api/v2/gocab/sign-up/token")
async def verify_signup_token(token: str):
    decoder = JwtDecoder
    result = decoder.decode_jwt(token)
    return JSONResponse({
        "result" : result
    })

@app.post("/api/v2/gocab/sign-up")
async def sign_up_api(request: Request) -> dict:
    # Getting the data from the request body
    logging.info("Starting API")
    json_data = await request.json()
    first_name = json_data.get("firstName")
    email = json_data.get("email")
    database = DatabaseHandler
    db_status = database.insert_signup_detail(json_data)
    if db_status:
        logging.info("Sign up details inserted in Database")
        jwt_encoder = JwtEncoder
        token = jwt_encoder.encode_for_minutes({
            "email" : email
        }, 5)
        # token_url = f"http://localhost:8000/api/v2/gocab/sign-up/token?token={token}"
        token_url = f"http://localhost:3000/verify/token/{token}"
        email_status = account_verify_sender(email, first_name, token_url)
        if email_status:
            logging.info("Mail sent")

    return JSONResponse({
                "status" : "success",
                "message" : "Account verification mail sent",
                "user" : email,
                "token" : token
            }, status_code= 200)
    

# redirect = f"http://localhost:3000/verify/token/{token}"