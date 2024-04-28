import random
import socket
import time
from rpi_remote_server.config import config


LOCAL_ADDRESS = '0.0.0.0'


def get_time():
    return time.time()


def get_secret_key():
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
