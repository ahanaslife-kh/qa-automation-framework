import logging
import os

def get_logger():
    os.makedirs("reports", exist_ok=True)

    logger = logging.getLogger("ixigo")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler("reports/test.log")
        formatter = logging.Formatter("%(asctime)s - %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
