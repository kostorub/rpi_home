from gpiozero import DigitalOutputDevice


class Relay(DigitalOutputDevice):
    def __init__(self, bcm_pin, phrase_on, phrase_off):
        self.phrase_on = phrase_on
        self.phrase_off = phrase_off
        super(Relay, self).__init__(bcm_pin)
