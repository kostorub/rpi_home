from gpiozero import Button as gpioButton

from gpiozero import DigitalOutputDevice


class Button(gpioButton):
    def __init__(self, bcm_pin, control_pin, name, relays):
        self.control_pin = control_pin
        self.name = name
        self.relays = relays
        super(Button, self).__init__(bcm_pin)

        self.when_pressed = self.pressed
        self.when_released = self.released

    def pressed(self):
        self.relays[self.control_pin].on()

    def released(self):
        self.relays[self.control_pin].off()
