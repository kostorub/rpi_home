import asyncore
import struct
import asyncio
from src.models.device_list import NoDevice

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
        data = await reader.read(20)
        addr = writer.get_extra_info("peername")
        print(f"Received {data} from {addr}")
        if data:
            try:
                bcm_pin, activate, get_status = struct.unpack(self.config["relays_struct"], data)
                relay = self.relays[bcm_pin]
                if get_status:
                    writer.write(struct.pack(self.config["relays_struct"], relay.pin.number, relay.value, False))
                else:
                    if activate:
                        relay.on()
                    else:
                        relay.off()
                    writer.write(self.pack_data(relay))
            except NoDevice:
                try:
                    bcm_pin, _, _ = struct.unpack(self.config["dht11s_struct"], data)
                    dht11 = self.dht11s[bcm_pin]
                    writer.write(struct.pack(self.config["dht11s_struct"], dht11.pin, dht11.status))
                except NoDevice as e:
                    print(e.message)
            await writer.drain()
        else:
            print("No data!")

        print("Close the client socket")
        writer.close()
