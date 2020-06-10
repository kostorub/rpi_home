import struct

from home_core.src.models.controller import Controller


class ControllerService(Controller):
    def __init__(self, bcm_pin, name=None):
        super(ControllerService).__init__(self, bcm_pin, name)
        self.relay = gpio.LED(bcm_pin)

    def unpack_data(self, value):
        data = struct.unpack(self.struct_template, value)
        bcm_pin = data[0]
        activate = data[1]
        if activate:
            self.on()
        else:
            self.off()

    def on(self):
        print(self, " on() method")
        self.relay.on()

    def off(self):
        print(self, " off() method")
        self.relay.off()
