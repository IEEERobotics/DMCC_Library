"""Library functions common to pyDMCC."""

import logging.handlers
import json
from os import path


_logger = None
_config = None
_config_file = None
_default_config = path.dirname(path.realpath(__file__))+"/default_config.json"

def get_config(config_file=_default_config):
    """Load and return configuration options.

    Note that this config is only loaded once (it's a singleton).

    :param config_file: JSON file to load config from.
    :type config_file: string
    :returns: Dict description of configuration.

    """
    # Don't load config file if it is already loaded (and filename matches)
    global _config, _config_file
    if _config is not None and config_file == _config_file:
        return _config
    _config_file = config_file

    # Build valid path from CWD to config file
    qual_config_file = config_file

    # Open and read config file
    with open(qual_config_file) as config_fd:
        return json.load(config_fd)


def get_logger():
    """Build and return a logger for formatted stream and file output.

    Note that if a logger has already been built, a new one will not
    be created. The previously created logger will be returned. This
    prevents running unnecessary setup twice, as well as premature logrolls.
    Two logger objects would not actually be created, as logger acts as
    a singleton.

    :returns: The constructed logging object.

    """
    # Don't run setup if logger has been built (would logroll early)
    global _logger
    if _logger is not None:
        return _logger

    # Get config so that path to log file can be read.
    config = get_config()

    # Get path from repo root to log file
    log_file = config["logging"]["log_file"]

    # Build logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Check if log exists and should therefore be rolled
    needRoll = False
    if path.isfile(log_file):
        needRoll = True

    # Build file output formatter
    file_formatter = logging.Formatter("%(asctime)s | %(levelname)s | "
                                       "%(filename)s | %(funcName)s | "
                                       "%(lineno)d | %(message)s")

    # Build stream output formatter
    stream_formatter = logging.Formatter("%(filename)s | %(funcName)s | "
                                         "%(lineno)d | %(levelname)s | "
                                         "%(message)s")

    # Build file handler (for output log output to files)
    file_handler = logging.handlers.RotatingFileHandler(log_file,
                                                        mode="a",
                                                        backupCount=50,
                                                        delay=True)
    file_handler_level = getattr(logging,
                         config["logging"]["file_handler_level"].upper(),
                         logging.DEBUG)
    file_handler.setLevel(file_handler_level)
    file_handler.setFormatter(file_formatter)

    # Build stream handler (for output to stdout)
    stream_handler = logging.StreamHandler()
    stream_handler_level = getattr(logging,
                           config["logging"]["stream_handler_level"].upper(),
                           logging.INFO)
    stream_handler.setLevel(stream_handler_level)
    stream_handler.setFormatter(stream_formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    # This is a stale log, so roll it
    if needRoll:
        logger.handlers[0].doRollover()

    logger.debug("Logger built")
    _logger = logger
    return logger
