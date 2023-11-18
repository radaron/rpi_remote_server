from flask import Blueprint, render_template


pages = Blueprint('pages', __name__)


@pages.route("/rpi/login", methods=['GET'])
def login_page():
    return render_template("index.html")

@pages.route("/rpi/manage", methods=['GET'])
def manage_page():
    return render_template("index.html")
