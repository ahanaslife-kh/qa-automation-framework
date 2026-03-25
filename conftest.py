
import os
from datetime import datetime
import pytest
from utils.driver_factory import  DriverFactory
import yaml

from utils.driver_factory import get_driver
from utils.screenshot_utils import take_screenshot
def load_config():
    with open("config.yaml", "r") as file:
        return yaml.safe_load(file)

@pytest.fixture(scope="session")
def config():
    return load_config()

@pytest.fixture(scope="function")
def driver():
    driver = get_driver()
    # Load base URL from config
    with open("config/config.yaml") as f:
        config = yaml.safe_load(f)

    driver.get(config["base_url"])
    yield driver
    driver.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver", None)
        if driver:
            take_screenshot(driver, item.name)
            try:
                if not os.path.exists("screenshots"):
                    os.makedirs("screenshots")
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                file_name = f"{item.name}_{timestamp}.png"
                file_path = os.path.join("screenshots", file_name)
                driver.save_screenshot(file_path)
                print(f"\n Screenshot saved: {file_path}")
            except Exception as e:
                print(f"\n Screenshot capture failed: {e}")
