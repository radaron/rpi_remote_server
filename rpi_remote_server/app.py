from datetime import timedelta
from flask import Flask
from flask_jwt_extended import JWTManager
from rpi_remote_server.database import init_db
from rpi_remote_server.util import get_secret_key
from rpi_remote_server.routes.api import api
from rpi_remote_server.routes.authentication import authentication, refresh_expiring_jwts
from rpi_remote_server.routes.pages import pages

app = Flask(__name__, static_url_path="/rpi/static")
app.config["JWT_SECRET_KEY"] = get_secret_key()
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)

app.register_blueprint(api)
app.register_blueprint(authentication)
app.register_blueprint(pages)
app.after_request(refresh_expiring_jwts)
init_db()


if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 8080, debug = True)
