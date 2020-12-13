import os

class Controller:
    def __init__(self, bcm_pin, name=None):
        self.pin = bcm_pin 
        self.state = False
        self.name = name

    def __repr__(self):
        return f"Class: {self.__class__.__name__}, name: {self.name}, status: {self.state}"

    def off(self):
        raise NotImplementedError

    def on(self):
        raise NotImplementedError


if __name__ == "__main__":
    controller = Controller(5)
    print(controller.name)
    controller = Controller(5)
    print(controller)
    print(controller.name)
    print(controller.state)
    controller.state = 1
    print(controller.state)
    controller.on()
    controller.off()
