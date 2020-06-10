from .controller import Controller


class ControllerList:
    def __init__(self, controllers=[]):
        self.controllers = controllers
    
    def __getitem__(self, value):
        for controller in self.controllers:
            if isinstance(value, str):
                if controller.name == value:
                    return controller
            if isinstance(value, int):
                if controller.pin == value:
                    return controller

if __name__ == "__main__":
    controllers = ControllerList()
    print(controllers[1])