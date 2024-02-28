import socket
from uuid import uuid4
import threading
import select
import sys
import argparse
import random
import requests
import paramiko
from rpi_remote_server.database import init_db, get_session, RpiOrder

HOST_KEY = paramiko.RSAKey.generate(1024)
SERVER_ADDRESS = "0.0.0.0"

init_db()

SERVER_USERNAME = str(uuid4().hex)[:5]
SERVER_PASSWORD = str(uuid4().hex)[:5]


def update_db_record(name, username, password, host, port, from_port, to_port):
    db_session = get_session()
    if record := db_session.get(RpiOrder, name):
        record.name = name
        record.username = username
        record.passwd = password
        record.host = host
        record.port = int(port)
        record.from_port = int(from_port)
        record.to_port = int(to_port)
        db_session.commit()
    db_session.close()


def delete_db_record(name):
    db_session = get_session()
    if record := db_session.get(RpiOrder, name):
        db_session.delete(record)
        db_session.commit()
    db_session.close()


def get_random_port():
    while True:
        port = random.randint(10000, 20000)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if not s.connect_ex(('127.0.0.1', port)) == 0:
                return port


def get_wan_ip_address():
    return requests.get("https://ifconfig.me", timeout=5).text


def get_lan_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_addr = s.getsockname()[0]
    s.close()
    return ip_addr


class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()
        self.listen = None
        self.to_port = None

    def check_auth_password(self, username, password):
        if username == SERVER_USERNAME and password == SERVER_PASSWORD:
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_port_forward_request(self, address, port):
        print(f"[*] Forwarding port {port}")
        self.to_port = port
        self.listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen.bind((SERVER_ADDRESS, int(port)))
        self.listen.listen(1)
        return self.listen.getsockname()[1]

    def cancel_port_forward_request(self, address, port):
        self.listen.close()
        self.listen = None

    def check_channel_request(self, kind, chanid):
        if kind in ["forwarded-tcpip", "session"]:
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED


def client_handler(client_socket):
    session_transport = paramiko.Transport(client_socket)
    session_transport.add_server_key(HOST_KEY)
    server = Server()
    try:

        session_transport.start_server(server=server)
    except paramiko.SSHException:
        print("[!] SSH Negotiation Failed")
        sys.exit(1)

    print("[*] SSH Negotiation Success")

    print("[*] Authenticating")
    session_chan = session_transport.accept(20)

    if session_chan is None or not session_chan.active:
        print("[!] Failure - SSH channel not active")
        session_transport.close()
    else:
        print("[*] Success - SSH channel active")
        print(f"[*] Waiting conenction on {get_lan_ip_address()}, {server.to_port}")
        while session_chan.active:
            try:
                try:
                    client_tunnel_socket, _ = server.listen.accept()
                except Exception:
                    print("[*] Closing associated channels")
                    session_transport.close()
                    break
                tunnel_chan = session_transport.open_forwarded_tcpip_channel(client_tunnel_socket.getsockname(), client_tunnel_socket.getpeername())
                while True:
                    r, _, _ = select.select([client_tunnel_socket, tunnel_chan], [], [])
                    if client_tunnel_socket in r:
                        data = client_tunnel_socket.recv(1024)
                        if len(data) == 0:
                            break
                        print(f"[*] Sending {len(data)} bytes via SSH Channel")
                        tunnel_chan.send(data)
                    if tunnel_chan in r:
                        data = tunnel_chan.recv(1024)
                        if len(data) == 0:
                            break
                        print(f"[*] Sending {len(data)} bytes via TCP Channel")
                        client_tunnel_socket.send(data)
            except Exception as err:
                print(f"[*] {err}")
                try:
                    print("[*] Closing associated sockets and channels")
                    client_tunnel_socket.close()
                    session_transport.close()
                except Exception:
                    pass


def main():
    parser = argparse.ArgumentParser(description='Start port forwarding with remote clients.')
    parser.add_argument('-n', '--name', metavar='NAME', type=str, required=True,
                        help='Name of client for connect')
    parser.add_argument('-p', '--port', type=int, required=True,
                        help='From port for forwarding from remote client.')
    args = parser.parse_args()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        ssh_port = get_random_port()

        server_socket.bind((SERVER_ADDRESS, ssh_port))
        server_socket.listen(20)

        ext_ip = get_wan_ip_address()
        to_port = get_random_port()
        print(f"[*] External address: {ext_ip} {ssh_port}")
        print(f"[*] Authentication username: {SERVER_USERNAME} password: {SERVER_PASSWORD}")
        print(f"[*] Forward client port: {args.port} to server port: {to_port}")
        update_db_record(args.name, SERVER_USERNAME, SERVER_PASSWORD, ext_ip, ssh_port, args.port, to_port)
        client_socket, addr = server_socket.accept()
        print(f"[*] Incoming TCP connection from {addr[0]}:{addr[1]}")
        client_handler(client_socket)
    except KeyboardInterrupt:
        print("[*] Exiting")
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        print("[*] Close socket")
        server_socket.close()
        delete_db_record(args.name)


if __name__ == "__main__":
    main()
