import logging
import sys

# Define logging format
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"


def get_logger(name: str = "fastapi-app") -> logging.Logger:
    """Configures and returns a logger instance."""
    logger = logging.getLogger(name)

    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(console_handler)

    return logger
