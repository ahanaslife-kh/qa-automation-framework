import os
from datetime import datetime

def take_screenshot(driver, name):
    if not os.path.exists("reports/screenshots"):
        os.makedirs("reports/screenshots")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"reports/screenshots/{name}_{timestamp}.png"

    driver.save_screenshot(file_path)
    return file_path
