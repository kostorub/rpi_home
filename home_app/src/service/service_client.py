import asyncore
import struct
from asyncore import poll

from kivy.clock import Clock

from src.common import config


class ServiceClient(asyncore.dispatcher):

    def __init__(self, host, port, controller, callback, **kwargs):
        asyncore.dispatcher.__init__(self)
        self.create_socket()
        self.connect( (host, port) )
        self.controller = controller
        self.callback = callback
        self.get_remote_status = kwargs.get("get_remote_status", 0)
        self.buffer = self.pack_data(controller)
        self.event = Clock.schedule_interval(poll, 0)

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()
        self.event.cancel()

    def handle_read(self):
        bcm_pin, state = self.unpack_data(self.recv(64))
        print(bcm_pin, state)
        self.callback(state)
        self.handle_close()

    def writable(self):
        return (len(self.buffer) > 0)

    def handle_write(self):
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]

    def pack_data(self, controller):
        return struct.pack(
            config["struct_template"], 
            controller.pin, 
            controller.state,
            self.get_remote_status)

    def unpack_data(self, value):
        data = struct.unpack(config["struct_template"], value)
        return data[0], data[1]
