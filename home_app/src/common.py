import os

from home_core.src.configuration.configuration import Configuration

config_path = os.environ.get("SERVER_CONFIG_PATH", "configuration/home_service")

config = Configuration(config_path, "server.yaml")
