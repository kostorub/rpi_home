import asyncore
import struct
import asyncio

class Server:
    def __init__(self, config, loop=None, **kwargs):
        self.loop = loop or asyncio.get_event_loop()
        self._coro = asyncio.start_server(self.handler, config["server"]["host"], int(config["server"]["port"]), loop=self.loop)
        self.config = config
        self.relays = kwargs.get("relays")
        self.dht11s = kwargs.get("dht11s")
    
    def start(self):
        self._server = self.loop.run_until_complete(self._coro)
        print('Serving on {}'.format(self._server.sockets[0].getsockname()))
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            # Close the server
            self._server.close()
            self.loop.run_until_complete(self._server.wait_closed())
            self.loop.close()


    async def handler(self, reader, writer):
        data = await reader.read(10)
        addr = writer.get_extra_info("peername")
        print(f"Received {data} from {addr}")
        if data:
            bcm_pin, activate, get_status = self.unpack_data(data)
            relay = self.relays[bcm_pin]
            if get_status:
                writer.write(self.pack_data(relay))
                await writer.drain()
            if activate:
                relay.on()
            else:
                relay.off()


        writer.write(self.pack_data(relay))
        await writer.drain()

        print("Close the client socket")
        writer.close()

    def unpack_data(self, value):
        data = struct.unpack(self.config["struct_template"], value)
        return data[0], data[1], data[2]

    def pack_data(self, relay):
        return struct.pack(self.config["struct_template"], relay.pin.number, relay.value, False)