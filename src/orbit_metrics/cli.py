import argparse
import logging


logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(description="Cosmos Exporter")

    parser.add_argument('--config',
                        type=str,
                        required=True,
                        action='store',
                        dest='config',
                        help='Path to the configuration file.')
    parser.add_argument('--log-file',
                        action='store',
                        dest='log_file',
                        default='orbit_metrics.log',
                        help='Set the log file path')
    parser.add_argument('--log-level',
                        action='store',
                        dest='log_level',
                        default='INFO',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help='Set the logging level.')

    args = parser.parse_args()
    logger.debug(f'Command line parameters: {args}')

    return args
