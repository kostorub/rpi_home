import gpiozero as gpio
import os

class Controller:
    __counter = -1

    def __init__(self, bcm_pin, name=None):
        self.relay = gpio.LED(bcm_pin)
        self.__name = name or f"{self.__class__.__name__}_{Controller._counter_()}"

    @property
    def name(self):
        return self.__name
    
    def state(self):
        return self.relay.value

    def pin(self):
        return self.relay.pin

    @staticmethod
    def _counter_():
        Controller.__counter += 1
        return Controller.__counter

    def __repr__(self):
        return f"Class: {self.__class__.__name__}, name: {self.name}, status: {self.state}"

    def off():
        raise NotImplementedError

    def on():
        raise NotImplementedError


if __name__ == "__main__":
    controller = Controller()
    print(controller.name)
    controller = Controller()
    print(controller)
    print(controller.name)
    print(controller.state)
    controller.state = 1
    print(controller.state)
    controller.on()
    controller.off()
