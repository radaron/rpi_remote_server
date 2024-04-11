# pylint: disable=wrong-import-position
import eventlet
eventlet.monkey_patch()

from flask_socketio import SocketIO, emit  # pylint: disable=import-error
from flask import Flask, send_from_directory, session
from rpi_remote_server.database import init_db, get_session, RpiOrder
from rpi_remote_server.forwarder import Forwarder
from rpi_remote_server.util import get_secret_key
from rpi_remote_server.config import config
from rpi_remote_server.routes.api import api
from rpi_remote_server.routes.authentication import authentication
from rpi_remote_server.routes.pages import pages

app = Flask(__name__, static_url_path="/rpi/static")
app.secret_key = get_secret_key()
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
socketio = SocketIO(app, cors_allowed_origins='*', async_mode='eventlet', path="/rpi/socket.io")

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


@socketio.on("start_forward")
def forward(event_body):
    client_name = event_body["name"]
    forwarder = Forwarder(client_name, config.host_name)  # pylint: disable=no-member
    for data in forwarder.forward():
        if data == 0:
            break
        if isinstance(data, str):
            emit('forward_resp', {"data": data})
        elif isinstance(data, dict):
            handle_connection(client_name, data["from"])
    handle_disconnection(client_name)
    emit('disconnect')


def handle_connection(client_name, port):
    app.logger.info("Client %s connected to port %s", client_name, port)
    db_session = get_session()
    if record := db_session.get(RpiOrder, client_name):
        record.name = client_name
        record.username = "username"
        record.passwd = "password"
        record.host = "host"
        record.port = int(port)
        record.from_port = 1
        record.to_port = 1
        db_session.commit()
        app.logger.info("Updated port %s for client %s", port, client_name)
    db_session.close()


def handle_disconnection(client_name):
    app.logger.info("Deleting record for client %s", client_name)
    db_session = get_session()
    if record := db_session.get(RpiOrder, client_name):
        db_session.delete(record)
        db_session.commit()
        app.logger.info("Deleted record for client %s", client_name)
    db_session.close()


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
