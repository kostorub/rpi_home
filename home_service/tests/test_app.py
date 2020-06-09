import socket
import struct
import pytest

host_ip, server_port = "127.0.0.1", 7272

MY_ROOM = 0
THE_CORRIDOR = 2
THE_BATH_LIGHT = 20

# Initialize a TCP client socket using SOCK_STREAM
tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Establish connection to TCP server and exchange data
    tcp_client.connect((host_ip, server_port))

    data = struct.pack("<h?", MY_ROOM, 1)
    print(data)

    tcp_client.sendall(data)

    # Read data from the TCP server and close the connection
    received = tcp_client.recv(1024)
finally:
    tcp_client.close()

print ("Bytes Sent:     {}".format(data))
print ("Bytes Received: {}".format(received.decode()))

from src.server import ControlServer
import asyncore

def test_app():
    server = ControlServer(config["server"]["host"], int(config["server"]["port"]))
    asyncore.loop()