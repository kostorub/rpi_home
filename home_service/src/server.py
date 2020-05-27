import asyncore
import struct


class ControlHandler(asyncore.dispatcher_with_send):

    def handle_read(self):
        data = self.recv(8192)
        print(data)
        if data:
            data = struct.unpack("<h?", data)
            print(data)
            self.send(str(data).encode())
        

class ControlServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.ignore_log_types = []
        self.create_socket()
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accepted(self, sock, addr):
        print('Incoming connection from %s' % repr(addr))
        handler = ControlHandler(sock)