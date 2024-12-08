"""
All front-end urls are generated here
"""

SERVER_HOST = "https://go-cab-ten.vercel.app"
LOCAL_HOST = "http://localhost:3000"

def forgot_password_url(token: str) -> str:
    """Return the URL for the forgot password page with the given token."""
    token_url: str = f"{SERVER_HOST}/verify/forget-password/token/{token}"
    return token_url

def account_verify_url(token: str) -> str:
    """Return the URL for the account verification page with the given token."""
    token_url: str = f"{SERVER_HOST}/verify/signup/token/{token}"
    return token_url