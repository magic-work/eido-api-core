import logging
import sys
from app.settings import get_settings

settings = get_settings()


class CustomFormatter(logging.Formatter):
    grey = '\x1b[38;21m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.grey + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def get_logger(name):
    log_format = " %(levelname)s - %(asctime)s %(name)s(%(lineno)d)::%(funcName)s - %(message)s "
    handler = logging.StreamHandler()
    handler.setFormatter(CustomFormatter(log_format))

    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(settings.log_level)
    logger.propagate = False

    if "pytest" in sys.modules:
        logger.setLevel(logging.CRITICAL)

    return logger
