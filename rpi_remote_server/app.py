from flask import Flask, send_from_directory, session
from rpi_remote_server.database import init_db
from rpi_remote_server.util import get_secret_key
from rpi_remote_server.routes.api import api
from rpi_remote_server.routes.authentication import authentication
from rpi_remote_server.routes.pages import pages

app = Flask(__name__, static_url_path="/rpi/static")
app.secret_key = get_secret_key()

app.register_blueprint(api)
app.register_blueprint(authentication)
app.register_blueprint(pages)
init_db()

@app.route('/rpi/favicon.ico')
def favicon():
    return send_from_directory('images', 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.before_request
def make_session_permanent():
    session.permanent = True


if __name__ == "__main__":
    app.run(host = "127.0.0.1", port = 8080, debug = True)
