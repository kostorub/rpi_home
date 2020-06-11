import asyncore

class ServiceClient(asyncore.dispatcher):

    def __init__(self, host, port, data: bytes):
        asyncore.dispatcher.__init__(self)
        self.create_socket()
        self.connect( (host, port) )
        self.buffer = data

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def handle_read(self):
        print(self.recv(8192))

    def writable(self):
        return (len(self.buffer) > 0)

    def handle_write(self):
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]
