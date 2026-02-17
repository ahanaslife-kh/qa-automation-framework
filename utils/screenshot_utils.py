import os
from datetime import datetime

def take_screenshot(driver, name="failure"):
    os.makedirs("reports/screenshots", exist_ok=True)
    file_name = f"reports/screenshots/{name}_{datetime.now().strftime('%H%M%S')}.png"
    driver.save_screenshot(file_name)
