import asyncore
import struct

from src.common import config
from src.service.service_client import ServiceClient


class DHT11ServiceClient(ServiceClient):
    def __init__(self, dht11, **kwargs):
        asyncore.dispatcher.__init__(self)
        self.dht11 = dht11
        self.buffer = self.pack_data(dht11)
        super(DHT11ServiceClient, self).__init__(**kwargs)

    def handle_read(self):
        bcm_pin, temperature, humidity = self.unpack_data(self.recv(64))
        print(temperature, humidity)
        self.callback(temperature, humidity)
        super().handle_read()

    def pack_data(self, dht11):
        print(dht11.bcm_pin)
        return struct.pack(config["dht11s_struct"], dht11.bcm_pin, -1, -1)

    def unpack_data(self, value):
        return struct.unpack(config["dht11s_struct"], value)
