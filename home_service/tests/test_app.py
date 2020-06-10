import os
import socket
import struct
from time import sleep

import pytest

from home_app.src.controller_app import ControllerApp
from home_core.src.configuration.configuration import Configuration
from home_core.src.models.controller_list import ControllerList

config_path = os.environ.get(
    "SERVER_CONFIG_PATH", "configuration/home_service")

config = Configuration(config_path, "server.yaml")

template = config["struct_template"]

controllers = ControllerList(
    [ControllerApp(
        binding["bcm_pin"], 
        binding["name"]
        ) for binding in config["bindings"]])

count = 5
while count:
    # Initialize a TCP client socket using SOCK_STREAM
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Establish connection to TCP server and exchange data
        tcp_client.connect(
            (config["server"]["host"], int(config["server"]["port"])))

        controller = controllers["Light test"]
        if controller.state:
            data = struct.pack(template, controller.pin, False)
        else:
            data = struct.pack(template, controller.pin, True)
        print(data)

        tcp_client.sendall(data)

        # Read data from the TCP server and close the connection
        received = tcp_client.recv(1024)
        data = struct.unpack(template, received)

        controllers[data[0]].state = data[1]
        property(controllers[data[0]])
    finally:
        tcp_client.close()

    sleep(2)
    count -= 1

print("Bytes Sent:     {}".format(data))
print("Bytes Received: {}".format(received.decode()))
