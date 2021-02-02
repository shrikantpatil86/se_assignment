import os
import config
import logging

from logging.handlers import RotatingFileHandler

class AppLogger(object):

    def __init__(self,module_name=__name__):
        self.module_name = module_name
        self.resource_name = os.environ["RESOURCE_NAME"]+".log"
        LOGGER = logging.getLogger(module_name)
        LOGGER.setLevel(config.LOG_LEVEL)
        log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        os.makedirs(config.LOG_DIR, exist_ok=True)
        file_handler = RotatingFileHandler(os.path.join(config.LOG_DIR, self.resource_name),
                                            maxBytes=200000, backupCount=10)
        file_handler.setFormatter(log_formatter)
        LOGGER.addHandler(file_handler)
        self.LOGGER = LOGGER

    def get_logger(self):
        return self.LOGGER

