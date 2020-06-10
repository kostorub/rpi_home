import asyncore
import struct

class ControlHandler(asyncore.dispatcher_with_send):

    def __init__(self, sock=None, map=None, controllers={}):
        super(ControlHandler, self).__init__(sock)
        self.controllers = controllers

    def handle_read(self):
        """
        Receives a data structure
        < - little-endian
        0 - h - integer (short 2 bytes) - id
        1 - ? - bool (Bool 1 byte) - on/off (0/1)
        """
        data = self.recv(8192)
        if data:
            data = struct.unpack("<h?", data)
            bcm_pin = data[0]
            activate = data[1]
            if activate:
                self.controllers[bcm_pin].on()
            else:
                self.controllers[bcm_pin].off()
            
            self.send(str(data).encode())
        

class ControlServer(asyncore.dispatcher):

    def __init__(self, host, port, **kwargs):
        asyncore.dispatcher.__init__(self)
        self.controllers = kwargs.get("controllers", {})
        self.ignore_log_types = []
        self.create_socket()
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accepted(self, sock, addr):
        print('Incoming connection from %s' % repr(addr))
        handler = ControlHandler(sock, controllers=self.controllers)