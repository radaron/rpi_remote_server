import json
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    unset_jwt_cookies
)
from rpi_remote_server.database import get_session, Authentication
from rpi_remote_server.authentication import validate_password


authentication = Blueprint('authentication', __name__)


@authentication.route("/rpi/token", methods=['POST'])
def token():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    db_session = get_session()

    if record := db_session.get(Authentication, username):
        if validate_password(password.encode(), record):
            access_token = create_access_token(identity=username)
            response = {"access_token": access_token}

            db_session.close()
            return response

    return {"msg": "Wrong email or password"}, 401


@authentication.route("/rpi/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response

def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        target_timestamp = datetime.timestamp(datetime.now() + timedelta(minutes=50))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if isinstance(data, dict):
                data["access_token"] = access_token
                response.data = json.dumps(data)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response
