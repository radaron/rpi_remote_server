import select
import socket
import json
from datetime import datetime
from rpi_remote_server.util import get_random_open_port, LOCAL_ADDRESS
from rpi_remote_server.config import config


class Forwarder:
    def __init__(self, name, connection_timeout=120):
        self._connection_timeout = connection_timeout
        self._name = name

    @staticmethod
    def log(msg):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"{timestamp} - {msg}"

    def _create_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((LOCAL_ADDRESS, get_random_open_port()))  # pylint: disable=no-member
        sock.settimeout(self._connection_timeout)
        sock.listen(1)
        return sock

    def _log_custom_messages(self, port):
        for message in json.loads(config.custom_messages):  # pylint: disable=no-member
            yield self.log(message.format(port=port))

    def forward(self):
        try:
            source_socket = self._create_socket()
            target_socket = self._create_socket()
            yield {"from": source_socket.getsockname()[1], "to": target_socket.getsockname()[1]}
            yield self.log(f'waiting for connection from {self._name} port: {source_socket.getsockname()[1]}')
            source_conn, source_addr = source_socket.accept()
            yield self.log(f"{self._name} connected from: {source_addr}")
            yield self.log(f'waiting for connection from user port: {target_socket.getsockname()[1]}')
            yield from self._log_custom_messages(target_socket.getsockname()[1])
            target_conn, target_addr = target_socket.accept()
            yield self.log(f"user connected from: {target_addr}")
            while True:
                rlist, _, _ = select.select([source_conn, target_conn], [], [])
                if source_conn in rlist:
                    data = source_conn.recv(4096)
                    yield self.log(f"received {len(data)} bytes data")
                    if len(data) == 0:
                        break
                    target_conn.sendall(data)
                if target_conn in rlist:
                    data = target_conn.recv(4096)
                    yield self.log(f"sent {len(data)} bytes data")
                    if len(data) == 0:
                        break
                    source_conn.sendall(data)
        except socket.timeout:
            yield self.log("Connection timeout")
        except Exception as e:  # pylint: disable=broad-except
            yield self.log(str(e))
        finally:
            source_socket.close()
            target_socket.close()
            yield self.log("Connection closed")
            yield 0