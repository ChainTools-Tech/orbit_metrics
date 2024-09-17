import logging
import time

from prometheus_client import start_http_server

from cosmos_exporter.cli import parse_args
from cosmos_exporter.config import load_config
from cosmos_exporter.exporter import fetch_metrics
from cosmos_exporter.logger import get_log_level, setup_logging


logger = logging.getLogger(__name__)


def main():
    args = parse_args()
    config = load_config(args.config)

    log_level = get_log_level(args.log_level)
    setup_logging(log_file=args.log_file, log_level=log_level)

    logger.info(f"Initializing application.")
    logger.debug(f'Command line arguments: {args}')

    start_http_server(8000)
    while True:
        fetch_metrics(config)
        time.sleep(60)  # Fetch metrics every 60 seconds


if __name__ == '__main__':
    main()