import os
import random
import socket
import time
import uuid


LOCAL_ADDRESS = '0.0.0.0'


def get_time():
    return time.time()


def generate_secret_key():
    with open("secret", "w", encoding="utf-8") as f:
        f.write(str(uuid.uuid4().hex))


def get_secret_key():
    if not os.path.exists("secret"):
        generate_secret_key()
    return open("secret", 'r', encoding="utf-8").read()


# pylint: disable=no-member
def get_random_open_port(port_start=int(config.port_range_start),
                         port_end=int(config.port_range_end),
                         local_address=LOCAL_ADDRESS):
    while True:
        port = random.randint(port_start, port_end)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex((local_address, port)) != 0:
                return port
