import socket

import bbb_hal.common as common


class Drive:

    def __init__(self, sock_path=None):
        config = common.load_config()
        if sock_path is None:
            self.sock_path  = config['server']['sock_path']
        else:
            self.sock_path = sock_path

        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect(self.sock_path)


