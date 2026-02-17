from utils.wait_utils import wait_for_visibility, wait_for_clickable
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    def __init__(self, driver):
        self.driver = driver

    def wait_for_visibility(self, locator, timeout=15):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def click_element(self, locator, timeout=15):
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()
    def enter_text(self, locator, text):
        element = wait_for_visibility(self.driver, locator)
        element.clear()
        element.send_keys(text)

