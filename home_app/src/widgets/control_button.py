import threading

from kivy.lang import Builder
from kivy.uix.button import Button

from src.common import config
from src.service.service_client import ServiceClient

Builder.load_file(__file__.replace(".py", ".kv"))

class ControlButton(Button):
    def __init__(self, **kwargs):
        self.controller = kwargs.pop("controller")
        super(ControlButton, self).__init__(**kwargs)

    def pressed(self):
        self.controller.state = False if self.controller.state else True
        ServiceClient(
            config["server"]["host"], 
            config["server"]["port"],
            self.controller,
            self.on_send)

    def on_send(self, state):
        self.controller.state = state
        if state:
            self.text = "[color=#00FF00]" + self.controller.name + "[/color]"
        else:
            self.text = "[color=#FF0000]" + self.controller.name + "[/color]"
