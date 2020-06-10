from src.server import ControlServer
import asyncore
from home_core.src.configuration.configuration import Configuration
from home_core.src.models.controller_list import ControllerList
from src.models.controller_service import ControllerService
import os


config_path = os.environ.get("SERVER_CONFIG_PATH", "configuration/home_service/server.yaml")

config = Configuration(config_path)

controllers = ControllerList([ControllerService(binding["bcm_pin"], binding["name"]) for binding in config["bindings"]])

server = ControlServer(config["server"]["host"], int(config["server"]["port"]), controllers=controllers)
asyncore.loop()