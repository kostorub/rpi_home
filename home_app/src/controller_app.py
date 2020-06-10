from home_core.src.models.controller import Controller
import struct
import socket

class ControllerApp(Controller):
    def pack_data(self, activate=False):
        data = struct.pack(self.struct_template, self.pin, activate)
        return data

    def on(self):
        # TODO implement message sending
        pass


    def off(self):
        # TODO implement message sending
        pass