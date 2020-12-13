import asyncio
from home_core.src.configuration.configuration import Configuration
from src.models.device_list import DeviceList
from src.models.relay import Relay
from gpiozero import Button
import os
import struct


config_path = os.environ.get("SERVER_CONFIG_PATH", "configuration/home_service")

config = Configuration(config_path, "server.yaml")

relays = DeviceList([Relay(relay["bcm_pin"], relay["phrase_on"], relay["phrase_off"]) for relay in config["relays"]])
buttons = DeviceList([Button(button["bcm_pin"]) for button in config["buttons"]])

async def control_server(reader, writer):
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


    writer.write(b"fff")
    await writer.drain()

    print("Close the client socket")
    writer.close()

def unpack_data(self, value):
    data = struct.unpack(config["struct_template"], value)
    return data[0], data[1], data[2]

def pack_data(self, relay):
    return struct.pack(config["struct_template"], relay.pin, relay.value, False)

loop = asyncio.get_event_loop()
coro = asyncio.start_server(control_server, config["server"]["host"], int(config["server"]["port"]), loop=loop)
server = loop.run_until_complete(coro)

print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()