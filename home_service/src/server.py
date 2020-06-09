import asyncore
import struct
import gpiozero

raspberry = False
try:
    gpiozero.pi_info()
    raspberry = True
except:
    print("This is not raspberry")

class ControlHandler(asyncore.dispatcher_with_send):

    def __init__(self, sock=None, map=None, config={}):
        super(ControlHandler, self).__init__(sock)
        self.config = config

    def handle_read(self):
        """
        Receives a data structure
        < - little-endian
        0 - h - integer (short 2 bytes) - id
        1 - ? - bool (Bool 1 byte) - on/off (0/1)
        """
        data = self.recv(8192)
        print(data)
        if data:
            data = struct.unpack("<h?", data)
            print(data)
            bcm_pin = self.config["bindings"][data[0]]["bcm_pin"]
            print(self.config["bindings"][data[0]])
            if raspberry:
                relay = gpiozero.LED(bcm_pin)
                if data[1]:
                    relay.on()
                else:
                    relay.off()
            
            self.send(str(data).encode())
        

class ControlServer(asyncore.dispatcher):

    def __init__(self, host, port, **kwargs):
        asyncore.dispatcher.__init__(self)
        self.config = kwargs.get("config", {})
        self.ignore_log_types = []
        self.create_socket()
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accepted(self, sock, addr):
        print('Incoming connection from %s' % repr(addr))
        # handler = ControlHandler(sock=sock, config=self.config)
        handler = ControlHandler(sock, config=self.config)