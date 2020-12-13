from gpiozero import DigitalOutputDevice


class Relay(DigitalOutputDevice):
    def __init__(self, bcm_pin, phrase_on, phrase_off, name):
        self.phrase_on = phrase_on
        self.phrase_off = phrase_off
        self.name = name
        super(Relay, self).__init__(bcm_pin)

    def on(self):
        super().on()
        print(self)

    def off(self):
        super().off()
        print(self)
