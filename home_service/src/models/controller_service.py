from home_core.src.models.controller import Controller

class ControllerService(Controller):
    def parse_data(value):
        data = struct.unpack(self.struct_template, value)
        bcm_pin = data[0]
        activate = data[1]
        if activate:
            self.on()
        else:
            self.off()

    def on():
        print(self, " on() method")
        self.relay.on()

    def off():
        print(self, " off() method")
        self.relay.off()