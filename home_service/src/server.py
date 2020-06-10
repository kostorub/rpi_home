import asyncore
import struct

class ControlHandler(asyncore.dispatcher_with_send):

    def __init__(self, sock=None, map=None, controllers={}):
        super(ControlHandler, self).__init__(sock)
        self.controllers = controllers

    def handle_read(self):
        data = self.recv(8192)
        if data:
            self.controllers[bcm_pin].parse_data(data)
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