import logging

logger = logging.getLogger("HAL.Robot")

config = None
bot = None


class Mock:

    def __init__(self, config):
        logger.info("Init MOCK robot interface")
        self.config = config


class Rover:
    def __init__(self, config):
        logger.info("Init ROVER interface")
        self.config = config


bot_classes = {
    "mock": Mock,
    "4x4 rover": Rover
}

def init(config_):
    logger.info("INIT robot")
    global config
    global bot

    config = config_

    bot_class = bot_classes[config["type"]]

    bot = bot_class(config)




