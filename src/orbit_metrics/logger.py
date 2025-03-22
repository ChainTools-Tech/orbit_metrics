import logging
import sys
import os
from typing import Optional, Union, List


def get_log_level(level_str: str) -> int:
    """
    Convert a string log level to the corresponding logging level.

    Args:
        level_str: String representation of the log level

    Returns:
        The logging level as an integer
    """
    try:
        return getattr(logging, level_str.upper())
    except AttributeError:
        logging.warning(f"Invalid log level '{level_str}', defaulting to INFO")
        return logging.INFO


def setup_logging(log_file: Optional[str] = None, log_level: int = logging.INFO) -> logging.Logger:
    """
    Set up logging with file and console handlers.

    Args:
        log_file: Path to the log file (or None to disable file logging)
        log_level: Logging level

    Returns:
        The configured root logger
    """
    # Create a clear, informative log format
    log_formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)-8s] %(name)s: (%(module)s, %(funcName)s): %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Get the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Remove all existing handlers to avoid duplicate messages
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Configure file handler if log_file is provided
    if log_file:
        try:
            # Ensure the directory exists
            log_dir = os.path.dirname(log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir, exist_ok=True)

            # Create the file handler
            file_handler = logging.FileHandler(filename=log_file, encoding='utf-8', mode='a')
            file_handler.setFormatter(log_formatter)
            root_logger.addHandler(file_handler)

            # Log message about where logs are being written
            root_logger.info(f"Logging to file: {os.path.abspath(log_file)}")
        except Exception as e:
            # If file logging fails, log to console
            console = logging.StreamHandler(sys.stderr)
            console.setFormatter(log_formatter)
            root_logger.addHandler(console)
            root_logger.error(f"Failed to set up log file ({log_file}): {e}")
            root_logger.error("Logging to console instead")

    # Configure console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_formatter)
    root_logger.addHandler(console_handler)

    return root_logger


def get_module_logger(module_name: str) -> logging.Logger:
    """
    Get a logger for a specific module.

    Args:
        module_name: Name of the module

    Returns:
        Logger for the module
    """
    return logging.getLogger(module_name)