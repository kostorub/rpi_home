from src.widgets.main import MainApp
from src.utils.kv_loader import load_all_kv
import os
from home_core.src.configuration.configuration import Configuration
from home_core.src.models.controller_list import ControllerList
from src.models.controller_app import ControllerApp


config_path = os.environ.get("SERVER_CONFIG_PATH", "configuration/home_service")

config = Configuration(config_path, "server.yaml")

controllers = ControllerList([ControllerApp(binding["bcm_pin"], binding["name"]) for binding in config["bindings"]])

load_all_kv(os.path.join("home_app", "src"))

app = MainApp(config=config, controllers=controllers)
app.run()
