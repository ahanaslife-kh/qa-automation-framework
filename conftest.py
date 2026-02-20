import pytest
import yaml

from utils.driver_factory import get_driver
from utils.screenshot_utils import take_screenshot


# ----------------------------
# BROWSER SETUP & TEARDOWN
# ----------------------------

@pytest.fixture(scope="function")
def driver():
    driver = get_driver()
    # Load base URL from config
    with open("config/config.yaml") as f:
        config = yaml.safe_load(f)

    driver.get(config["base_url"])
    yield driver
    driver.quit()


# ----------------------------
# SCREENSHOT ON FAILURE
# ----------------------------

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if driver:
            take_screenshot(driver, item.name)
