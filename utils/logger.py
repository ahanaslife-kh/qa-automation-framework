import logging
import os
from datetime import datetime

# Create directories
LOG_DIR = "reports/logs"
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs("logs", exist_ok=True)

# Optional basic setup (from your version)
def setup_logger():
    logging.basicConfig(
        filename="logs/test.log",
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

def get_logger(name="ixigo"):
    log_file = os.path.join(
        LOG_DIR,
        f"execution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    )

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        # File handler (dynamic log file)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)

        # Console handler (from your version)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger