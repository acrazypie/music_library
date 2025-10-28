from flask_restful import reqparse, fields
from dotenv import load_dotenv
import os
import jwt
from datetime import datetime, timedelta

load_dotenv()

user_args = reqparse.RequestParser()
user_args.add_argument("name", type=str, required=True, help="Name cannot be blank")
user_args.add_argument("email", type=str, required=True, help="Email cannot be blank")

useFields = {
    "id": fields.Integer,
    "name": fields.String,
    "email": fields.String,
}


class Config:
    # Flask settings
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Google Login
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    REDIRECT_URI = "http://localhost:5000/auth/callback"
    SCOPE = os.getenv("SCOPE")
    AUTH_BASE_URL = os.getenv("AUTH_BASE_URL")
    TOKEN_URL = os.getenv("TOKEN_URL")
    USER_INFO_URL = os.getenv("USER_INFO_URL")


config = Config()


def create_jwt(user, expires_in=3600, refresh=False):
    payload = {
        "sub": user.google_id,
        "email": user.email,
        "type": "refresh" if refresh else "access",
        "exp": datetime.utcnow() + timedelta(seconds=expires_in),
    }
    token = jwt.encode(payload, config.SECRET_KEY or "dev", algorithm="HS256")
    return token


def verify_jwt(token, expected_type="access"):
    try:
        payload = jwt.decode(token, config.SECRET_KEY or "dev", algorithms=["HS256"])
        if payload.get("type") != expected_type:
            return None
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
