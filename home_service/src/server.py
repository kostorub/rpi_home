import asyncore
import struct
import asyncio

class Server:
    def __init__(self, host, port, loop=None, **kwargs):
        self._loop = loop or asyncio.get_event_loop()
        self._coro = asyncio.start_server(self.handler, host, port, loop=self._loop)
    
    def start(self):
        self._server = self._loop.run_until_complete(self._coro)
        print('Serving on {}'.format(self._server.sockets[0].getsockname()))
        try:
            self._loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            # Close the server
            self._server.close()
            self._loop.run_until_complete(self._server.wait_closed())
            self._loop.close()


    async def handler(reader, writer):
        data = await reader.read(10)
        addr = writer.get_extra_info('peername')
        print(f"Received {data} from {addr}")
        if data:
            bcm_pin, activate, get_status = unpack_data(data)
            relay = relays[bcm_pin]
            if get_status:
                writer.write(pack_data(relay))
                await writer.drain()
            if activate:
                relay.on()
            else:
                relay.off()


        writer.write(pack_data(relay))
        await writer.drain()

        print("Close the client socket")
        writer.close()

    def unpack_data(value):
        data = struct.unpack(config["struct_template"], value)
        return data[0], data[1], data[2]

    def pack_data(relay):
        return struct.pack(config["struct_template"], relay.pin, relay.value, False)