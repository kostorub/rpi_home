import struct

import gpiozero as gpio

from home_core.src.models.controller import Controller


class ControllerService(Controller):
    def __init__(self, bcm_pin, name=None):
        super(ControllerService, self).__init__(bcm_pin, name)
        self.relay = gpio.LED(bcm_pin)

    def on(self):
        print(self, " on() method")
        self.relay.on()
        self.state = 1

    def off(self):
        print(self, " off() method")
        self.relay.off()
        self.state = 0
