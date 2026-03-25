import os
from datetime import datetime
import pytest
import yaml
from utils.driver_factory import get_driver
from utils.screenshot_utils import take_screenshot

# ---------- CONFIG LOADER ----------
def load_config():
    with open("config/config.yaml", "r") as file:
        return yaml.safe_load(file)

@pytest.fixture(scope="session")
def config():
    return load_config()

# ---------- DRIVER FIXTURE ----------
@pytest.fixture(scope="function")
def driver():
    driver = get_driver()

    # Load base URL from config
    config = load_config()
    driver.get(config["base_url"])

    yield driver
    driver.quit()

# ---------- PYTEST HOOK ----------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    # attach report to item (from server version)
    setattr(item, "rep_" + rep.when, rep)

    # take screenshot on failure
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver", None)
        if driver:
            try:
                # primary method (utility)
                file_path = take_screenshot(driver, item.name)
                print(f"\n📸 Screenshot saved: {file_path}")
            except Exception:
                # fallback method (your version)
                try:
                    os.makedirs("screenshots", exist_ok=True)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    file_path = os.path.join("screenshots", f"{item.name}_{timestamp}.png")
                    driver.save_screenshot(file_path)
                    print(f"\n📸 Screenshot saved (fallback): {file_path}")
                except Exception as e:
                    print(f"\n❌ Screenshot capture failed: {e}")