from src.service.relay_service_client import RelayServiceClient


class Relay:
    def __init__(self, bcm_pin, phrase_on, phrase_off, name):
        self.bcm_pin = bcm_pin
        self.phrase_on = phrase_on
        self.phrase_off = phrase_off
        self.name = name
        self.button = None

    def on(self, **kwargs):
        self.state = True
        self.sevice_run(**kwargs)

    def off(self, **kwargs):
        self.state = False
        self.sevice_run(**kwargs)

    def sevice_run(self, **kwargs):
        RelayServiceClient(self, callback=kwargs.get("on_send"))

