#standard python libs
import logging
import time

#third party libs
from daemon import runner

import bbb_hal.server as server

class App():

    def __init__(self, logger, path):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/var/run/bbb-hal/bbb-hal.pid'
        self.pidfile_timeout = 5
        self.logger = logger
        self.sock_path = path

    def run(self):
        #while True:
            #Main code goes here ...
            #Note that logger level needs to be set to logging.DEBUG before this shows up in the logs
            #logger.debug("Debug message")
            #logger.info("Info message")
            #logger.warn("Warning message")
            #logger.error("Error message")
            #time.sleep(10)
        server.init_and_run(self.logger, self.sock_path)


logger = logging.getLogger("DaemonLog")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("/var/log/bbb-hal/bbb-hal.log")
handler.setFormatter(formatter)
logger.addHandler(handler)

app = App(logger, "/var/run/bbb-hal/bbb-hal.sock")

daemon_runner = runner.DaemonRunner(app)
#This ensures that the logger file handle does not get closed during daemonization
daemon_runner.daemon_context.files_preserve=[handler.stream]
daemon_runner.do_action()
