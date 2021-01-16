import asyncio
from src.models.configuration import Configuration
from src.models.device_list import DeviceList
from src.models.relay import Relay
from src.server import Server
from gpiozero import Button
import os
import struct


config_path = os.environ.get("SERVER_CONFIG_PATH", "configuration/home_service")
config = Configuration(config_path, "server.yaml")

relays = DeviceList([
    Relay(
        relay["bcm_pin"],
        relay["phrase_on"],
        relay["phrase_off"],
        relay["name"]) for relay in config["relays"]])

buttons = DeviceList([Button(button["bcm_pin"]) for button in config["buttons"]])

server = Server(config["server"]["host"], int(config["server"]["port"]), relays=relays)
server.start()
