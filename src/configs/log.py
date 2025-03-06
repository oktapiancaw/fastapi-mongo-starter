import os
import logging
import logging.config

from enum import Enum
from logging.handlers import RotatingFileHandler


class CustomLogLevel(int, Enum):
    NOTSET = 0
    DEBUG = 10
    CONNECTION = 15
    INFO = 20
    SUCCESS = 25
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


# Create logs directory if it doesn't exist
if not os.path.exists("./logs"):
    os.mkdir("./logs")

# Define a custom log level names
logging.addLevelName(CustomLogLevel.SUCCESS, "SUCCESS")
logging.addLevelName(CustomLogLevel.CONNECTION, "CONNECTION")


class ColoredTerminalFormatter(logging.Formatter):
    debug = "\x1b[38;2;122;115;209m"
    connection = "\x1b[38;2;181;168;213m"
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    green = "\x1b[32m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format_str = "{}%(levelname)s:{}%(filename)s:%(lineno)d - %(message)s{}"

    FORMATS = {
        logging.DEBUG: format_str.format(debug, "\t", reset),
        logging.INFO: format_str.format(grey, "\t", reset),
        logging.WARNING: format_str.format(yellow, "\t", reset),
        logging.ERROR: format_str.format(red, "\t", reset),
        logging.CRITICAL: format_str.format(bold_red, "\t", reset),
        CustomLogLevel.SUCCESS: format_str.format(green, "\t", reset),
        CustomLogLevel.CONNECTION: format_str.format(connection, "\t", reset),
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


# Define the log configuration dictionary
LOGCONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "colored": {
            "()": ColoredTerminalFormatter,  # Adjust to your actual class path if needed
        },
        "default": {
            "format": "[%(levelname)s] %(asctime)s - %(filename)s:%(module)s:%(funcName)s:%(lineno)d - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "colored",
            "level": CustomLogLevel.INFO,
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "./logs/app.log",
            "maxBytes": 1048576,
            "backupCount": 4,
            "formatter": "default",
            "level": CustomLogLevel.CONNECTION,  # You can set this to the lowest level for broader capture
        },
        "full_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "./logs/full_app.log",
            "maxBytes": 5242880,
            "backupCount": 2,
            "formatter": "default",
            "level": CustomLogLevel.DEBUG,  # You can set this to the lowest level for broader capture
        },
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["console", "file", "full_file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

# Load the logging configuration
logging.config.dictConfig(LOGCONFIG)


# Create custom logging methods
def success(self, message, *args, **kws):
    if self.isEnabledFor(CustomLogLevel.SUCCESS):
        self._log(CustomLogLevel.SUCCESS, message, args, **kws)


def connection(self, message, *args, **kws):
    if self.isEnabledFor(CustomLogLevel.CONNECTION):
        self._log(CustomLogLevel.CONNECTION, message, args, **kws)


logging.Logger.success = success  # type: ignore
logging.Logger.connection = connection  # type: ignore

# Create a logger instance
LOGGER = logging.getLogger(__name__)
