import socket
import struct

from home_core.src.models.controller import Controller
from src.common import config
from src.service.service_client import ServiceClient


class ControllerApp(Controller):
    __button = None

    def __init__(self, bcm_pin, phrase_on, phrase_off, name=None):
        self.__phrase_on = phrase_on
        self.__phrase_off = phrase_off
        super(ControllerApp, self).__init__(bcm_pin, name)

    @property
    def button(self):
        return self.__button

    @button.setter
    def button(self, value):
        self.__button = value

    def on(self, **kwargs):
        self.state = True
        self.sevice_init(**kwargs)

    def off(self, **kwargs):
        self.state = False
        self.sevice_init(**kwargs)

    def sevice_init(self, **kwargs):
        ServiceClient(
            config["server"]["host"],
            config["server"]["port"],
            self,
            kwargs.get("on_send"))

    @property
    def phrase_on(self):
        return self.__phrase_on

    @property
    def phrase_off(self):
        return self.__phrase_off
