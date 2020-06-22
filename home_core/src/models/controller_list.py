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
    
    def __iter__(self):
        return iter(self.controllers)

    def find_similar_phrase(self, text):
        phrases = text.split()
        for controller in self.controllers:
            if all(phrase in controller.phrase_on for phrase in phrases):
                return controller, True
            if all(phrase in controller.phrase_off for phrase in phrases):
                return controller, False
        return None, False

if __name__ == "__main__":
    controllers = ControllerList()
    print(controllers[1])