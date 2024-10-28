import smtplib
from email.mime.text import MIMEText
from Emails.MailLayouts import *
from Configuration.config import *

# This function is responsible for sending OTP to users via email
def send_otp_by_mail(recipient:str, user_first_name:str, OTP:int):
    try:
        logging.info(f"Sending OTP via mail to {recipient}")
        # Getting HTML layout for sending OTP
        html_body = otp_mail_layout(user_first_name, OTP)
        # Create MIMEText object with 'html' MIME type
        msg = MIMEText(html_body, 'html')
        msg['Subject'] = f"OTP for registration"
        msg['From'] = EMAIL_SENDER
        msg['To'] = recipient
        # Connecting with SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_SENDER_PASSWORD)
            server.sendmail(EMAIL_SENDER, recipient, msg.as_string())
        return True
    except Exception as error:
        logging.error(f"ERROR OCCURED WHILE SENDING OTP TO {recipient} :" f"{error}")
        return False
    
    
# This function is responsible for sending a confirmation emails to users 
def registration_success_mail(recipient:str, user_first_name:str):
    try:
        logging.info(f"Sending confirmation e-mail to {recipient}")
        # Getting HTML layout for registration success
        html_body = confirmation_mail_layout(user_first_name)
        # Create MIMEText object with 'html' MIME type
        msg = MIMEText(html_body, 'html')
        msg['Subject'] = f"Registration successfull."
        msg['From'] = EMAIL_SENDER
        msg['To'] = recipient
        # Connecting with SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_SENDER_PASSWORD)
            server.sendmail(EMAIL_SENDER, recipient, msg.as_string())
        return True
    except Exception as error:
        logging.error(f"ERROR OCCURED WHILE SENDING CONFIRMATION TO {recipient} :" f"{error}")
        return False    
    
    
# This function is responsible for sending OTP to password change
def forgot_password_otp_send(user_email:str, user_first_name:str, OTP:int):
    try:
        logging.info(f"Sending OTP via mail to {user_email}")
        # Getting HTML layout for sending OTP
        html_body = forgot_password_mail_layout(user_first_name, OTP)
        # Create MIMEText object with 'html' MIME type
        msg = MIMEText(html_body, 'html')
        msg['Subject'] = f"OTP for changing password"
        msg['From'] = EMAIL_SENDER
        msg['To'] = user_email
        # Connecting with SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_SENDER_PASSWORD)
            server.sendmail(EMAIL_SENDER, user_email, msg.as_string())
        return True
    except Exception as error:
        logging.error(f"ERROR OCCURED WHILE SENDING OTP FOR CHANGING PASSWORD TO {user_email} :" f"{error}")
        return False    