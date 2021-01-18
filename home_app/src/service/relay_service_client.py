import asyncore
import struct

from src.common import config
from src.service.service_client import ServiceClient


class RelayServiceClient(ServiceClient):
    def __init__(self, relay, **kwargs):
        asyncore.dispatcher.__init__(self)
        self.relay = relay
        self.get_remote_status = kwargs.get("get_remote_status", 0)
        self.buffer = self.pack_data(relay)
        super(RelayServiceClient, self).__init__(**kwargs)

    def handle_read(self):
        bcm_pin, state = self.unpack_data(self.recv(64))
        print(bcm_pin, state)
        self.callback(state)
        super().handle_read()

    def pack_data(self, controller):
        return struct.pack(
            config["relays_struct"], 
            controller.pin, 
            controller.state,
            self.get_remote_status)

    def unpack_data(self, value):
        return struct.unpack(config["relays_struct"], value)
