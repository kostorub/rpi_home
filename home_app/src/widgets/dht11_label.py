from kivy.lang import Builder
from kivy.uix.label import Label

from src.common import config
from src.service.dht11_service_client import DHT11ServiceClient

Builder.load_file(__file__.replace(".py", ".kv"))

class DHT11Label(Label):
    def __init__(self, **kwargs):
        self.dht11 = kwargs.pop("dht11")
        self.dht11.label = self
        super(DHT11Label, self).__init__(**kwargs)

    def pressed(self):
        self.get_remote_state()

    def on_send(self, temperature, humidity):
        self.text = f"Temp: {temperature}C Hum: {humidity}%"

    def get_remote_state(self):
        DHT11ServiceClient(
            self.dht11,
            callback=self.on_send)
