import smtplib
from email.mime.text import MIMEText
from Emails.MailLayouts import *
from Configuration.config import *

# This function is responsible for sending OTP to users via email
def account_verify_sender(user_email: str, first_name: str, token_url: str) -> bool:
    """
    This function sends account verification Email.
    
    Args
    ----
        >>>
    user_email (str): Email of user.
    first_name (str): First name of user.
    token_url  (str): Token URL with JWT.
    
    Returns
    -------
        >>> 
    bool: True if email sent successfully, False otherwise.
    """
    try:
        mail = SendEmailLayout
        logging.info(f"Sending account verification email to : {user_email}")
        # Getting HTML layout for sending email
        html_body = mail.verify_account_layout(first_name, token_url)
        # Create MIMEText object with 'html' MIME type
        msg = MIMEText(html_body, 'html')
        msg['Subject'] = f"Account verify"
        msg['From'] = EMAIL_SENDER
        msg['To'] = user_email
        # Connecting with SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_SENDER_PASSWORD)
            server.sendmail(EMAIL_SENDER, user_email, msg.as_string())
            logging.info(f"Account verification email sent to : {user_email}")
        return True
    except Exception as error:
        logging.error(f"ERROR OCCURED WHILE SENDING OTP TO {user_email} :" f"{error}")
        return False