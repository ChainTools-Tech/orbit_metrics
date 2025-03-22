import logging
import signal
import sys
import time
from typing import Dict, Any

from prometheus_client import start_http_server

from orbit_metrics.cli import parse_args
from orbit_metrics.config import load_config, validate_config
from orbit_metrics.exporter import fetch_metrics
from orbit_metrics.logger import get_log_level, setup_logging

logger = logging.getLogger(__name__)

# Flag to control the main loop
running = True


def signal_handler(sig, frame):
    """Handle termination signals gracefully."""
    global running
    logger.info(f"Received signal {sig}, shutting down...")
    running = False


def main():
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Parse arguments and load configuration
    args = parse_args()
    try:
        config = load_config(args.config)
        validate_config(config)
    except Exception as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)

    # Setup logging
    log_level = get_log_level(args.log_level)
    setup_logging(log_file=args.log_file, log_level=log_level)

    logger.info("Initializing orbit_metrics application")
    logger.debug(f'Command line arguments: {args}')

    # Get prometheus port from config or use default
    prometheus_port = config.get('prometheus', {}).get('port', 8000)

    try:
        # Start Prometheus HTTP server
        start_http_server(prometheus_port)
        logger.info(f"Prometheus metrics server started on port {prometheus_port}")

        # Get metrics refresh interval from config or use default (60 seconds)
        refresh_interval = config.get('refresh_interval', 60)
        logger.info(f"Metrics refresh interval set to {refresh_interval} seconds")

        # Main loop
        global running
        while running:
            try:
                fetch_metrics(config)
            except Exception as e:
                logger.error(f"Error fetching metrics: {e}")

            # Sleep for the refresh interval or until a signal is received
            for _ in range(refresh_interval):
                if not running:
                    break
                time.sleep(1)

    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

    logger.info("Application shutdown complete")


if __name__ == '__main__':
    main()