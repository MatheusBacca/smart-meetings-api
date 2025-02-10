import logging
from logging.handlers import RotatingFileHandler
import os

from configobj import ConfigObj


config = ConfigObj("config.cfg")


def setup_logger(
    name=__name__,
    log_file=config["LOGS"]["FILE_NAME"],
    level=logging.DEBUG,
    max_bytes=10 * 1024 * 1024,  # 10 MB or 10.485.760 bytes
    backup_count=config["LOGS"]["BACKUP_COUNT"],
):
    """
    Configure a reusable logger.

    Args:
        name (str): Logger name.
        log_file (str): Log file name.
        level (int): Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        max_bytes (int): Max log file length before rotational.
        backup_count (int): Old backup logs number.

    Returns:
        logging.Logger: Configurated logger instance.
    """

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] [%(name)s:%(funcName)s:%(lineno)d] %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    os.makedirs("logs", exist_ok=True)

    file_handler = RotatingFileHandler(
        f"logs/{log_file}", maxBytes=max_bytes, backupCount=backup_count
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


if __name__ == "__main__":
    api_logger = setup_logger()
    api_logger.info("Logger configurated successfully!")
    api_logger.debug("Debug log test.")
    api_logger.warning("Warning log test!")
    api_logger.error("Error log test.")
    api_logger.critical("Critical log test")
