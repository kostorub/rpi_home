import os
import socket
import struct
from time import sleep

import pytest
from home_service.src.models.device_list import DeviceList
from home_service.src.models.relay import Relay
from home_core.src.configuration.configuration import Configuration


config_path = os.environ.get(
    "SERVER_CONFIG_PATH", "configuration/home_service")

config = Configuration(config_path, "server.yaml")

template = config["struct_template"]

controllers = DeviceList()

for item in config["relays"]:
    relay = Relay(
        item["bcm_pin"], 
        item["phrase_on"],
        item["phrase_off"])
    relay.name = item["name"]
    relay.value = 1
    relay.pin = 5
    controllers.append(relay)


count = 5
while count:
    # Initialize a TCP client socket using SOCK_STREAM
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Establish connection to TCP server and exchange data
        tcp_client.connect(
            (config["server"]["host"], int(config["server"]["port"])))

        controller = controllers["Light test"]
        if controller.value:
            data = struct.pack(template, controller.pin, False, False)
        else:
            data = struct.pack(template, controller.pin, True, False)
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
