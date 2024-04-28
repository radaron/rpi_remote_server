from flask_socketio import emit
from rpi_remote_server.database import get_session, RpiOrder
from rpi_remote_server.forwarder import Forwarder


class ForwardAdapter:

    def __init__(self, client_name, logger):
        self._client_name = client_name
        self._logger = logger

    def start(self):
        forwarder = Forwarder(self._client_name)
        for data in forwarder.forward():
            if data == 0:
                break
            if isinstance(data, str):
                emit('forward_resp', {"data": data})
            elif isinstance(data, dict):
                self._handle_connection(data["from"])
        self._handle_disconnection()
        emit('disconnect')

    def _handle_connection(self, port):
        self._logger.info("Prepare client %s connection to port %s", self._client_name, port)
        db_session = get_session()
        if record := db_session.get(RpiOrder, self._client_name):
            record.name = self._client_name
            record.username = "username"
            record.passwd = "password"
            record.host = "host"
            record.port = int(port)
            record.from_port = 1
            record.to_port = 1
            db_session.commit()
            self._logger.info("Updated port %s for client %s", port, self._client_name)
        db_session.close()

    def _handle_disconnection(self):
        self._logger.info("Deleting record for client %s", self._client_name)
        db_session = get_session()
        if record := db_session.get(RpiOrder, self._client_name):
            db_session.delete(record)
            db_session.commit()
            self._logger.info("Deleted record for client %s", self._client_name)
        db_session.close()
