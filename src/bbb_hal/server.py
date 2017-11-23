import asyncio
import logging

import bbb_hal.robot as robot

logger = logging.getLogger("HAL.Server")
config = None


class HalProtocol(asyncio.Protocol):

    def connection_made(self, transport):
        logger.info("1234")
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))

        print('Send: {!r}'.format(message))
        self.transport.write(data)

        print('Close the client socket')
        self.transport.close()

def start(config_):
    global config
    config = config_

    logger.info("Starting server on {}".format(config["sock_path"]))
    loop = asyncio.get_event_loop()
    # Each client connection will create a new protocol instance
    coro = loop.create_unix_server(HalProtocol, config["sock_path"])
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

def stop():
    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
