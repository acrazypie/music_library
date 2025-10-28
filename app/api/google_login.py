from flask import redirect, request, jsonify, session
from flask_restful import Resource
from requests_oauthlib import OAuth2Session
from ..utility import config
from app.models import db
from app.models.user import UserModel
from ..utility import create_jwt, verify_jwt


class GoogleLogin(Resource):
    def get(self):
        google = OAuth2Session(
            config.GOOGLE_CLIENT_ID,
            scope=config.SCOPE,
            redirect_uri=config.REDIRECT_URI,
        )
        authorization_url, state = google.authorization_url(
            config.AUTH_BASE_URL or "", access_type="offline", prompt="consent"
        )
        session["oauth_state"] = state
        return redirect(authorization_url)


class GoogleCallback(Resource):
    def get(self):
        google = OAuth2Session(
            config.GOOGLE_CLIENT_ID,
            state=session["oauth_state"],
            redirect_uri=config.REDIRECT_URI,
        )
        token = google.fetch_token(
            config.TOKEN_URL or "",
            client_secret=config.GOOGLE_CLIENT_SECRET,
            authorization_response=request.url,
        )
        userinfo = google.get(config.USER_INFO_URL or "").json()

        # Store or update user
        user = UserModel.query.filter_by(google_id=userinfo["id"]).first()
        if not user:
            user = UserModel()
            user.google_id = userinfo["id"]
            user.email = userinfo["email"]
            user.username = userinfo.get("name")
            user.picture = userinfo.get("picture")

            db.session.add(user)

        # Generate refresh token (valid 30 days)
        refresh_token = create_jwt(user, expires_in=60 * 60 * 24 * 30, refresh=True)
        user.refresh_token = refresh_token
        db.session.commit()

        # Access token (valid 1 hour)
        access_token = create_jwt(user, expires_in=60 * 60)

        return jsonify(
            {
                "message": "Login successful",
                "user": {
                    "name": user.username,
                    "email": user.email,
                    "picture": user.picture,
                },
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
        )


class RefreshToken(Resource):
    def post(self):
        data = request.get_json()
        token = data.get("refresh_token")
        if not token:
            return {"error": "Missing refresh_token"}, 400

        payload = verify_jwt(token, expected_type="refresh")
        if not payload:
            return {"error": "Invalid or expired refresh token"}, 401

        user = UserModel.query.filter_by(google_id=payload["sub"]).first()
        if not user or user.refresh_token != token:
            return {"error": "Refresh token not valid"}, 401

        # Issue new access token
        new_access_token = create_jwt(user, expires_in=60 * 60)
        return {"access_token": new_access_token}


class ProtectedResource(Resource):
    def get(self):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return {"error": "Missing token"}, 401

        token = auth_header.split(" ")[1]
        payload = verify_jwt(token)
        if not payload:
            return {"error": "Invalid or expired token"}, 401

        return {"message": f"Hello, {payload['email']}! Your token is valid."}
