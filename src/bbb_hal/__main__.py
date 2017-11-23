#standard python libs
import logging
import json
import time

#third party libs
from daemon import runner

import bbb_hal.server as server
import bbb_hal.robot as robot

class App():

    def __init__(self, config):
        self.config = config
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/var/run/bbb-hal/bbb-hal.pid'
        self.pidfile_timeout = 5

    def run(self):
        robot.init(self.config["robot"])
        server.start(self.config["server"])


logger = logging.getLogger("HAL")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("/var/log/bbb-hal/bbb-hal.log")
handler.setFormatter(formatter)
logger.addHandler(handler)


def load_config():
    with open("/usr/local/etc/bbb-hal.conf", 'r') as conf_file:
        config = json.load(conf_file)
    return config


app = App(load_config())

daemon_runner = runner.DaemonRunner(app)
#This ensures that the logger file handle does not get closed during daemonization
daemon_runner.daemon_context.files_preserve=[handler.stream]
daemon_runner.do_action()
