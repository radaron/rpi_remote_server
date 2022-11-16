import paramiko
import socket
from datetime import datetime
import hashlib
import threading
import select
import uuid
import sys

host_key = paramiko.RSAKey.generate(1024)
server_address = "0.0.0.0"
server_port = int(sys.argv[1])

date_now = datetime.now()
server_username = hashlib.sha256(f"{date_now.year}{date_now.month}".encode()).hexdigest()[:5]
server_password = hashlib.sha256(f"{date_now.day}{date_now.hour}".encode()).hexdigest()[:10]

class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()
    def check_auth_password(self, username, password):
        if username == server_username and password == server_password:
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED
    def check_port_forward_request(self, addr, port):
        print(f"[*] Forwarding port {port}")
        self.listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen.bind(("127.0.0.1", int(port)))
        self.listen.listen(1)
        return self.listen.getsockname()[1]
    def cancel_port_forward_request(self, addr, port):
        self.listen.close()
        self.listen = None
    def check_channel_request(self, kind, chanid):
        if kind in ["forwarded-tcpip", "session"]:
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

def client_handler(client_socket):
    session_transport = paramiko.Transport(client_socket)
    session_transport.add_server_key(host_key)
    server = Server()
    try:
        session_transport.start_server(server=server)
    except SSHException as err:
        print(f"[!] SSH Negotiation Failed")
        sys.exit(1)

    print(f"[*] SSH Negotiation Success")

    print("[*] Authenticating")
    session_chan = session_transport.accept(20)

    if session_chan == None or not session_chan.active:
        print("[!] Failure - SSH channel not active")
        session_transport.close()
    else:
        print("[*] Success - SSH channel active")
        while session_chan.active:
            try:
                try:
                    client_tunnel_socket, addr = server.listen.accept()
                except:
                    print("[*] Closing associated channels")
                    session_transport.close()
                    break
                print(f"[*] Incoming tunneled conenction from {addr[0]}:{addr[1]}")
                tunnel_chan = session_transport.open_forwarded_tcpip_channel(client_tunnel_socket.getsockname(), client_tunnel_socket.getpeername())
                while True:
                    r, w, x = select.select([client_tunnel_socket, tunnel_chan], [], [])
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
            except (paramiko.SSHException, Exception) as err:
                print("[*] ", str(err))
                try:
                    print("[*] Closing associated sockets and channels")
                    client_tunnel_socket.close()
                    session_transport.close()
                except:
                    pass

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server_socket.bind((server_address, server_port))
except:
    print("[!] Bind Error")
    sys.exit(1)

print(f"[*] Bind Success {server_address}:{server_port}")
print(f"[*] Authentication username: {server_username}, password: {server_password}")
server_socket.listen(20)

try:
    client_socket, addr = server_socket.accept()
    print(f"[*] Incoming TCP connection from {addr[0]}:{addr[1]}")
    client_handler(client_socket)
finally:
    server_socket.close()