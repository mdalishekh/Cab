import smtplib
from email.mime.text import MIMEText
from Emails.MailLayouts import *
from Configuration.config import *

# This function is responsible for sending signup verification to users via email
def signup_verify_sender(user_email: str, first_name: str, token_url: str) -> bool:
    """
    This function sends signup verification Email.
    
    Args
    ----
        user_email (str): Email of user.
        first_name (str): First name of user.
        token_url  (str): Token URL with JWT.
    
    Returns
    ------- 
        (bool)
    """
    try:
        mail = SendEmailLayout
        logging.info(f"Sending signup verification email to : {user_email}")
        # Getting HTML layout for sending email
        html_body = mail.signup_verify_layout(first_name, token_url)
        # Create MIMEText object with 'html' MIME type
        msg = MIMEText(html_body, 'html')
        msg['Subject'] = f"Email verification for signup"
        msg['From'] = EMAIL_SENDER
        msg['To'] = user_email
        # Connecting with SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_SENDER_PASSWORD)
            server.sendmail(EMAIL_SENDER, user_email, msg.as_string())
        return True
    except Exception as error:
        logging.error(f"error occurred while sending signup verification email to  {user_email} :  {error}")
        return False
    
    
    
# This function is responsible for sending forget password verification to users via email
def forgot_password_verify_sender(user_email: str, first_name: str, token_url: str) -> bool:
    """
    This function sends forget password verification Email.
    
    Args
    ----
        user_email (str): Email of user.
        first_name (str): First name of user.
        token_url  (str): Token URL with JWT.
    
    Returns
    ------- 
        (bool)
    """
    
    try:
        mail = SendEmailLayout
        logging.info(f"Sending signup verification email to : {user_email}")
        # Getting HTML layout for sending email
        html_body = mail.forgot_password_verify_layout(first_name, token_url)
        # Create MIMEText object with 'html' MIME type
        msg = MIMEText(html_body, 'html')
        msg['Subject'] = f"Forgot password email verification"
        msg['From'] = EMAIL_SENDER
        msg['To'] = user_email
        # Connecting with SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_SENDER_PASSWORD)
            server.sendmail(EMAIL_SENDER, user_email, msg.as_string())
        return True
    except Exception as error:
        logging.error(f"error occurred while sending forgot password verification email to  {user_email} :  {error}")
        return False    