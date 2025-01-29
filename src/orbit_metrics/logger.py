import logging
import sys


def get_log_level(level_str):
    try:
        return getattr(logging, level_str.upper())
    except AttributeError:
        return logging.INFO


def setup_logging(log_file, log_level=logging.INFO):
    log_formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)-8s] %(name)s: (%(module)s, %(funcName)s): %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Get the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Remove all existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Configure file handler if log_file is provided
    if log_file:
        file_handler = logging.FileHandler(filename=log_file, encoding='utf-8', mode='w')
        file_handler.setFormatter(log_formatter)
        root_logger.addHandler(file_handler)

    # Configure console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_formatter)
    root_logger.addHandler(console_handler)

    return root_logger