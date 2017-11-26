import asyncio
import logging

import bbb_hal

import bbb_hal.robot as robot
import bbb_hal.frames as frames

logger = logging.getLogger("HAL.Server")
config = None

class DriveProtocol(asyncio.Protocol):

    def __init__(self, transport, pkt, proto_switch):
        logger.info("Swithed to the Drive protocol!")

class NewConnProtocol(asyncio.Protocol):

    known_protos = {
        bbb_hal.frames.InitDrive: DriveProtocol,
    }

    def __init__(self, transport, proto_switch):
        logger.info("init new connection protocl")
        self.transport = transport
        self.proto_switch = proto_switch

    def data_received(self, data):
        logger.info("handling in new_conn handler")

        logger.info("Starting pkt parsing")
        pkt, remainder = frames.unpack(data)
        logger.info("Finished pkt parsing")

        logger.info("Pkt type: {}".format(type(pkt)))
        logger.info("known protos {}".format(NewConnProtocol.known_protos))
        if type(pkt) not in self.known_protos:

            logger.info("unknown init packet.")
            self.transport.close()


        logger.info("known protos {}".format(self.known_protos))
        if type(pkt) in self.known_protos:

            logger.info("Pkt type is: {}".format(type(pkt)))
            proto_class = self.known_protos[type(pkt)]
        else:
            logger.info("not in known protos ! ")

        proto_class = DriveProtocol
        logger.info("Proto class is : {}".format(proto_class))

        self.proto_switch.proto = proto_class(self.transport, pkt,
                                              self.proto_switch)





class ProtocolSwitch(asyncio.Protocol):

    def connection_made(self, transport):
        logger.info("New connection!")
        self.transport = transport
        self.proto = NewConnProtocol(self.transport, self)

    def data_received(self, data):
        logger.info("{} Bytes Recv".format(len(data)))
        self.proto.data_received(data)
        #message = data.decode()
        #print('Data received: {!r}'.format(message))

        #print('Send: {!r}'.format(message))
        #self.transport.write(data)

        #print('Close the client socket')
        #self.transport.close()

    def connection_lost(self, exc):
        logger.info("CONNECTION LOST")
        self.proto.connection_lost(exc)



def start(config_):
    global config
    config = config_

    logger.info("Starting server on {}".format(config["sock_path"]))
    loop = asyncio.get_event_loop()
    # Each client connection will create a new protocol instance
    coro = loop.create_unix_server(ProtocolSwitch, config["sock_path"])
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
