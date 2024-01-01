from flask import Blueprint, request, jsonify, session, redirect
from rpi_remote_server.database import get_session, Authentication
from rpi_remote_server.authentication import validate_password


authentication = Blueprint('authentication', __name__)


@authentication.route("/rpi/session", methods=['POST'])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    db_session = get_session()

    if record := db_session.get(Authentication, username):
        if validate_password(password.encode(), record):
            session['username'] = username

            db_session.close()
            return redirect("/rpi/manage")

    return {"msg": "Wrong email or password"}, 401


@authentication.route("/rpi/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    session.pop('username', None)
    return redirect("/rpi/login")
