import select
import socket
from datetime import datetime
from flask_socketio import emit
from rpi_remote_server.database import get_session, RpiOrder
from rpi_remote_server.util import get_random_open_port, LOCAL_ADDRESS
from rpi_remote_server.config import CUSTOM_MESSAGES


class Forwarder:

    def __init__(self, client_name, logger, connection_timeout=120):
        self._client_name = client_name
        self._logger = logger
        self._connection_timeout = connection_timeout

    def get_client_username(self):
        db_session = get_session()
        order = db_session.get(RpiOrder, self._client_name)
        db_session.close()
        return order.username if order and order.username else '<unknown>'

    @staticmethod
    def _log(msg):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        emit('forward_resp', {"data": f"{timestamp} - {msg}"})

    def _create_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((LOCAL_ADDRESS, get_random_open_port()))  # pylint: disable=no-member
        sock.settimeout(self._connection_timeout)
        sock.listen(1)
        return sock

    def _log_custom_messages(self, port):
        for message in CUSTOM_MESSAGES:  # pylint: disable=no-member
            self._log(message.format(username=self.get_client_username(), port=port))

    def start(self):
        try:
            source_socket = self._create_socket()
            target_socket = self._create_socket()
            self._handle_connection(source_socket.getsockname()[1])
            self._log(
                f'waiting for connection from {self._client_name}'
                f' port: {source_socket.getsockname()[1]}'
            )
            source_conn, source_addr = source_socket.accept()
            self._log(f"{self._client_name} connected from: {source_addr}")
            self._log(f'waiting for connection from user port: {target_socket.getsockname()[1]}')
            self._log_custom_messages(target_socket.getsockname()[1])
            target_conn, target_addr = target_socket.accept()
            self._log(f"user connected from: {target_addr}")
            while True:
                rlist, _, _ = select.select([source_conn, target_conn], [], [])
                if source_conn in rlist:
                    data = source_conn.recv(4096)
                    self._log(f"received {len(data)} bytes data")
                    if len(data) == 0:
                        break
                    target_conn.sendall(data)
                if target_conn in rlist:
                    data = target_conn.recv(4096)
                    self._log(f"sent {len(data)} bytes data")
                    if len(data) == 0:
                        break
                    source_conn.sendall(data)
        except socket.timeout:
            self._log("Connection timeout")
        except Exception as e:  # pylint: disable=broad-except
            self._log(str(e))
        finally:
            source_socket.close()
            target_socket.close()
            self._log("Connection closed")
            self._handle_disconnection()
            emit('disconnect')

    def _handle_connection(self, port):
        self._logger.info("Prepare client %s connection to port %s", self._client_name, port)
        db_session = get_session()
        if record := db_session.get(RpiOrder, self._client_name):
            record.name = self._client_name
            record.port = int(port)
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
