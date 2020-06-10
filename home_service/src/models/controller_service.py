from home_core.src.models.controller import Controller

class ControllerService(Controller):
    def on():
        print(self, " on() method")
        self.relay.on()

    def off():
        print(self, " off() method")
        self.relay.off()