import argparse
import logging
import os
from typing import List, Optional, Any

logger = logging.getLogger(__name__)


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Parse command line arguments.

    Args:
        args: Command line arguments (or None to use sys.argv)

    Returns:
        Parsed command line arguments
    """
    parser = argparse.ArgumentParser(
        description="Orbit Metrics - Prometheus exporter for Cosmos SDK blockchains",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        '--config',
        type=str,
        required=True,
        action='store',
        dest='config',
        help='Path to the configuration file.'
    )

    parser.add_argument(
        '--log-file',
        action='store',
        dest='log_file',
        default='orbit_metrics.log',
        help='Set the log file path'
    )

    parser.add_argument(
        '--log-level',
        action='store',
        dest='log_level',
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Set the logging level.'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 0.1.0'
    )

    parsed_args = parser.parse_args(args)

    # Validate the config file path
    if not os.path.exists(parsed_args.config):
        parser.error(f"Config file not found: {parsed_args.config}")

    logger.debug(f'Command line parameters: {parsed_args}')

    return parsed_args