import os
from asyncore import poll, socket_map
from functools import partial

from kivy.clock import Clock

from home_core.src.configuration.configuration import Configuration
from home_core.src.models.controller_list import ControllerList
from src.models.controller_app import ControllerApp
from src.utils.kv_loader import load_all_kv
from src.widgets.main import MainApp

config_path = os.environ.get("SERVER_CONFIG_PATH", "configuration/home_service")

config = Configuration(config_path, "server.yaml")

controllers = ControllerList([ControllerApp(binding["bcm_pin"], binding["name"]) for binding in config["bindings"]])

load_all_kv(os.path.join("home_app", "src"))

Clock.schedule_interval(poll, 0.1)

app = MainApp()
app.run()
