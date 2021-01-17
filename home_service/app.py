import asyncio
from functools import partial
from src.models.configuration import Configuration
from src.models.device_list import DeviceList
from src.models.relay import Relay
from src.server import Server
from src.models.button import Button
from src.speech_recognition import SpeechRecognition
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

buttons = DeviceList([
    Button(
        button["bcm_pin"],
        button["control_pin"],
        button["name"],
        relays) for button in config["buttons"]])

loop = asyncio.get_event_loop()

model_path = os.environ.get("MODEL_PATH", "home_service/model")
sr = SpeechRecognition(model_path, config, relays, loop)

server = Server(config, loop, relays=relays)
server.start()
