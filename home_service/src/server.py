import asyncore
import struct


class ControlHandler(asyncore.dispatcher_with_send):

    def __init__(self, sock=None, map=None, **kwargs):
        super(ControlHandler, self).__init__(sock)
        self.controllers = kwargs.get("controllers")
        self.config = kwargs.get("config")
        self.template = self.config["struct_template"]

    def handle_read(self):
        data = self.recv(8192)
        if data:
            bcm_pin, activate = self.unpack_data(data)
            if activate:
                self.controllers[bcm_pin].on()
            else:
                self.controllers[bcm_pin].off()

            self.send(pack_data())

    def unpack_data(self, value):
        data = struct.unpack(self.template, value)
        return data[0], data[1]

    def pack_data(self, controller, activate):
        return struct.pack(self.template, controller.pin, controller.state)


class ControlServer(asyncore.dispatcher):

    def __init__(self, host, port, **kwargs):
        asyncore.dispatcher.__init__(self)
        self.controllers = kwargs.get("controllers")
        self.config = kwargs.get("config")
        self.ignore_log_types = []
        self.create_socket()
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accepted(self, sock, addr):
        print('Incoming connection from %s' % repr(addr))
        handler = ControlHandler(
            sock, 
            config=self.config, 
            controllers=self.controllers)
