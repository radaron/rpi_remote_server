# pylint: disable=wrong-import-position
import eventlet

eventlet.monkey_patch()

from flask_socketio import SocketIO  # pylint: disable=import-error
from flask import Flask, send_from_directory
from rpi_remote_server.database import init_db
from rpi_remote_server.util import get_secret_key, create_admin_user
from rpi_remote_server.routes.api import api
from rpi_remote_server.routes.authentication import authentication
from rpi_remote_server.routes.pages import pages
from rpi_remote_server.forwarder import Forwarder


app = Flask(__name__, static_url_path="/static")
app.secret_key = get_secret_key()
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet", path="/socket.io")

app.register_blueprint(api)
app.register_blueprint(authentication)
app.register_blueprint(pages)
init_db()
create_admin_user()


@app.route("/favicon.ico")
def favicon():
    return send_from_directory("images", "favicon.ico", mimetype="image/vnd.microsoft.icon")


@socketio.on("start_forward")
def forward(event_body):
    adapter = Forwarder(event_body["name"], app.logger)
    adapter.start()


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
