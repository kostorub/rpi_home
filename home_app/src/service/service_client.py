import asyncore
import struct
from asyncore import poll

from kivy.clock import Clock

from src.common import config


class ServiceClient(asyncore.dispatcher):

    def __init__(self,**kwargs):
        asyncore.dispatcher.__init__(self)
        self.create_socket()
        self.connect( (config["server"]["host"], config["server"]["port"]) )
        self.callback = kwargs.get("callback")
        self.event = Clock.schedule_interval(poll, 0)

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()
        self.event.cancel()

    def handle_read(self):
        self.handle_close()

    def writable(self):
        return (len(self.buffer) > 0)

    def handle_write(self):
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]

    def pack_data(self, controller):
        raise NotImplementedError

    def unpack_data(self, value):
        raise NotImplementedError
