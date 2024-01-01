from flask import Blueprint, render_template, session, redirect
from rpi_remote_server.authentication import verify_username


pages = Blueprint('pages', __name__)


@pages.route("/rpi/login", methods=['GET'])
def login_page():
    return render_template("index.html")

@pages.route("/rpi/manage", methods=['GET'])
def manage_page():
    if verify_username(session.get('username')):
        return render_template("index.html")
    return redirect("/rpi/login")
