from src.server import ControlServer
import asyncore
from src.configuration.configuration import Configuration
import os


config_path = os.environ.get("SERVER_CONFIG_PATH", "configuration/home_service/server.yaml")

config = Configuration(config_path)
server = ControlServer(config["server"]["host"], int(config["server"]["port"]), config=config)
asyncore.loop()