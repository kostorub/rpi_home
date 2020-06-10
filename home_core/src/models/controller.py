import os

class Controller:
    __counter = -1

    def __init__(self, bcm_pin, name=None):
        self.__pin = bcm_pin 
        self.__state = 0
        self.__name = name or f"{self.__class__.__name__}_{Controller._counter_()}"

    @property
    def name(self):
        return self.__name
    
    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, value):
        self.__state = value

    @property
    def pin(self):
        return self.__pin

    @staticmethod
    def _counter_():
        Controller.__counter += 1
        return Controller.__counter

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
