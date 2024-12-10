# This module is specially made for sending mails to users for OTP verifications

# Class of all Email sending layout
class SendEmailLayout:
    """
    This Class contain some function which returns Email layouts for sending Email.
    """
    # This function returns Account Verify layout
    def signup_verify_layout(first_name: str,
                              token_url: str
                              ) -> str:
        """
        This function returns Account Verify layout.
        
        Args:
            >>> 
        first_name (str): First name of the user.
        token_url  (str): Url with JWT verification.
        >>>
            
        Returns:
            >>> Email layout (str)
        """
        # Email layout for signup verification
        layout = f"""
                    <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Verify Your Email Address</title>
                </head>
                <body style="margin: 0; padding: 0; background-color: #f0f0f0; font-family: system-ui, -apple-system, sans-serif;">
                    <table width="100%" cellpadding="0" cellspacing="0" border="0">
                        <tr>
                            <td align="center" style="padding: 40px 20px;">
                                <table width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width: 640px;">
                                    <tr>
                                        <td align="center" bgcolor="#ffffff" style="border-radius: 8px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); padding: 40px 20px;">
                                            <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                                <tr>
                                                    <td align="center" style="padding-bottom: 24px;">
                                                        <h3 style="color: #0f0f0f; font-size: 28px; margin: 0;">Hi {first_name}!</h3>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td align="center" style="padding-bottom: 8px;">
                                                        <h2 style="color: #0f0f0f; font-size: 24px; margin: 0;">Verify Your Email Address</h2>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td align="center" style="padding-bottom: 32px;">
                                                        <p style="color: #666666; font-size: 16px; line-height: 24px; margin: 0;">
                                                            Thanks for signing up! Please verify your email address by clicking the button below.
                                                        </p>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td align="center" style="padding-bottom: 32px;">
                                                        <a href="{token_url}" style="background-color: #2563eb; color: #ffffff; padding: 12px 24px; border-radius: 6px; text-decoration: none; font-size: 16px; font-weight: 500; display: inline-block;" target="_blank">
                                                            Verify Account
                                                        </a>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td align="center" style="padding-bottom: 32px;">
                                                        <p style="color: #666666; font-size: 14px; line-height: 20px; margin: 0;">
                                                            This email is valid for only 5 minutes
                                                        </p>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td align="center" style="border-top: 1px solid #e5e7eb; padding-top: 32px;">
                                                        <p style="color: #666666; font-size: 12px; line-height: 16px; margin: 0;">
                                                            This is an automated email. Please do not reply to this email.
                                                        </p>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                    </table>
                </body>
                </html>
                        
        """
        return layout
    
    
    def forgot_password_verify_layout(first_name: str,
                              token_url: str
                              ) -> str:
        """
        This function returns Account Verify layout.
        
        Args:
            >>> 
        first_name (str): First name of the user.
        token_url  (str): Url with JWT verification.
        >>>
            
        Returns:
            >>> Email layout (str)
        """
        # Email layout for forgot password verification
        layout = f"""
                    <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Verify Your Email Address</title>
                </head>
                <body style="margin: 0; padding: 0; background-color: #f0f0f0; font-family: system-ui, -apple-system, sans-serif;">
                    <table width="100%" cellpadding="0" cellspacing="0" border="0">
                        <tr>
                            <td align="center" style="padding: 40px 20px;">
                                <table width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width: 640px;">
                                    <tr>
                                        <td align="center" bgcolor="#ffffff" style="border-radius: 8px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); padding: 40px 20px;">
                                            <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                                <tr>
                                                    <td align="center" style="padding-bottom: 24px;">
                                                        <h3 style="color: #0f0f0f; font-size: 28px; margin: 0;">Hey {first_name}!</h3>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td align="center" style="padding-bottom: 8px;">
                                                        <h2 style="color: #0f0f0f; font-size: 24px; margin: 0;">Verify Your Email Address</h2>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td align="center" style="padding-bottom: 32px;">
                                                        <p style="color: #666666; font-size: 16px; line-height: 24px; margin: 0;">
                                                            We've been requested to change your password! Please click the button below to verify it's you.
                                                        </p>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td align="center" style="padding-bottom: 32px;">
                                                        <a href="{token_url}" style="background-color: #2563eb; color: #ffffff; padding: 12px 24px; border-radius: 6px; text-decoration: none; font-size: 16px; font-weight: 500; display: inline-block;" target="_blank">
                                                            Verify Email
                                                        </a>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td align="center" style="padding-bottom: 32px;">
                                                        <p style="color: #666666; font-size: 14px; line-height: 20px; margin: 0;">
                                                            This email is valid for only 5 minutes
                                                        </p>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td align="center" style="border-top: 1px solid #e5e7eb; padding-top: 32px;">
                                                        <p style="color: #666666; font-size: 12px; line-height: 16px; margin: 0;">
                                                            This is an automated email. Please do not reply to this email.
                                                        </p>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                    </table>
                </body>
                </html>
                        
        """
        return layout