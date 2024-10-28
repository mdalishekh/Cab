# This module is specially made for sending mails to users for OTP verifications

# This function is responsible for sending mails to users for OTP verifications layout
def otp_mail_layout(user_first_name, OTP):
    otp_layout  = f'''
                 <!DOCTYPE html>
                <html lang="en">
                <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>OTP Email Template</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
        }}
        .container {{
            background-color: #ffffff;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            overflow: hidden;
            width: 100%;
            max-width: 400px;
            margin: 0 auto; /* Centering the container */
            padding: 20px;
        }}
        .header {{
            background-color: #020c0d;
            color: #ffffff;
            padding: 20px;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            border-radius: 4px;
        }}
        .content {{
            padding: 20px;
            text-align: center;
        }}
        .otp-container {{
            background-color: #020c0d;
            color: #ffffff;
            font-size: 24px;
            font-weight: bold;
            padding: 10px;
            margin: 20px auto;
            border-radius: 4px;
            width: 130px;
        }}
        .expiry-note {{
            font-size: 14px;
            color: #666666;
            margin-top: 20px;
        }}
        .footer {{
            font-size: 12px;
            color: #999999;
            text-align: center;
            padding: 10px;
            border-top: 1px solid #eeeeee;
        }}
    </style>
</head>
<body>
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f4f4f4; padding: 20px;">
        <tr>
            <td align="center">
                <div class="container">
                    <div class="header">Hi, {user_first_name}</div>
                    <div class="content">
                        <p>Your One Time Password is here below</p>
                        <div class="otp-container">{OTP}</div>
                        <p class="expiry-note">Please note this OTP will expire in 5 minutes</p>
                    </div>
                    <div class="footer">
                        This is an automated email. Please do not reply.
                    </div>
                </div>
            </td>
        </tr>
    </table>
</body>
</html>

'''
    return otp_layout

# This function is responsible for sending mails to users for Registration confirmation layout
def confirmation_mail_layout(user_first_name):
    confirmation_layout = f"""
                           <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Confirmation Email</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;  /* Changed to greyish background for the body */
            margin: 0;
            padding: 20px;  /* Added padding to body for proper spacing */
        }}
        .container {{
            background-color: white;  /* Set white background for the template */
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            padding: 20px;
            max-width: 400px;
            margin: 0 auto; /* Centering the container */
            text-align: center;
        }}
        .header {{
            background-color: #020c0d;
            color: white;
            padding: 15px;
            font-size: 1.2em;
            font-family: Geneva, Tahoma, sans-serif;
            border-radius: 8px 8px 0 0;
        }}
        .content {{
            margin: 20px 0;
        }}
        .created-account {{
            background-color: #020c0d;
            color: white;
            padding: 10px;
            font-size: 1em;
            font-family: Geneva, Tahoma, sans-serif;
            border-radius: 4px;
            width: 80%;
            margin: 10px auto;
        }}
        .footer {{
            font-size: 0.9em;
            color: #777;
            margin-top: 20px;
        }}
        .footer-line {{
            border-top: 1px solid #ddd;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">Confirmation Email</div>
        <div class="content">
            <p>Congratulations, {user_first_name} You have been successfully registered.</p>
            <div class="created-account">Your account has been created!</div>
            <p>Thank you for joining us. We're excited to have you on board.</p>
        </div>
        <div class="footer">
            <div class="footer-line"></div>
            <p>This is an automated email. Please do not reply.</p>
        </div>
    </div>
</body>
</html>
                           """
    return confirmation_layout

def forgot_password_mail_layout(user_first_name, OTP):
    forgot_layout = f"""
                     <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Change OTP</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #aaa7a7; /* Greyish background */
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            min-width: 320px;
        }}
        .email-container {{
            background-color: #ffffff;
            max-width: 400px;
            width: 100%; /* Makes sure it adapts to different screen sizes */
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2); /* Added box-shadow */
            text-align: center;
            margin: 0 auto; /* Ensures centering on desktop */
        }}
        .email-header {{
            background-color: #000000;
            color: #ffffff;
            padding: 20px;
            font-size: 20px;
            font-weight: bold;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            margin: 0; /* Remove margin */
        }}
        .email-body {{
            padding: 20px 20px 0 20px;
            color: #333;
        }}
        .otp-box {{
            background-color: #000000;
            color: #ffffff;
            display: inline-block;
            padding: 10px 40px; 
            font-size: 24px;
            font-weight: bold;
            border-radius: 4px;
            margin: 20px 0;
        }}
        .email-footer {{
            border-top: 1px solid #e0e0e0;
            padding-top: 10px;
            font-size: 12px;
            color: #888888;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="email-container">
        <div class="email-header">
            Dear, {user_first_name}
        </div>
        <div class="email-body">
            <p style="padding-top: -3px;">We have been requested to change your password.<br><br>
            Please use the OTP below to confirm it's you:</p>
            <div class="otp-box">{OTP}</div>
            
            <p>Please note this OTP will expire in 5 minutes</p>
        </div>
        <div class="email-footer">
            This is an automated email. Please do not reply.
        </div>
    </div>
</body>
</html>

                     """
    return forgot_layout