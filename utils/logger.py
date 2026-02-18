import logging
import os

def get_logger():
    os.makedirs("reports", exist_ok=True)

    logger = logging.getLogger("ixigo")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter("%(asctime)s - %(message)s")

        # File handler
        file_handler = logging.FileHandler("reports/test.log")
        file_handler.setFormatter(formatter)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
