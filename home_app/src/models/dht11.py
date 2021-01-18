from src.service.dht11_service_client import DHT11ServiceClient


class DHT11:
    def __init__(self, bcm_pin, phrase, name):
        self.bcm_pin = bcm_pin
        self.phrase = phrase
        self.name = name
        self.lable = None

    def sevice_run(self, **kwargs):
        DHT11ServiceClient(self, callback=kwargs.get("on_send"))

