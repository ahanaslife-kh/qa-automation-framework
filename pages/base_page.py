import time

from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from utils.logger import get_logger


class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        self.logger = get_logger(self.__class__.__name__)
    # ----------------------------
    # BASIC ELEMENT ACTIONS
    # ----------------------------

    def click_element(self, locator):
        self.logger.info(f"Clicking element: {locator}")
        self.wait.until(EC.element_to_be_clickable(locator)).click()
        time.sleep(2)

    def enter_text(self, locator, text):
        self.logger.info(f"Entering text '{text}' into {locator}")
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)
        time.sleep(1)

    def get_text(self, locator):
        self.logger.info(f"Getting text from {locator}")
        return self.wait.until(
            EC.visibility_of_element_located(locator)
        ).text

    def is_visible(self, locator):
        self.logger.info(f"Checking visibility of {locator}")
        self.wait.until(EC.visibility_of_element_located(locator))
        return True

    # ----------------------------
    # WAIT HELPERS
    # ----------------------------

    def wait_for_presence(self, locator):
        self.logger.info(f"Waiting for presence of {locator}")
        return self.wait.until(
            EC.presence_of_element_located(locator)
        )

    def wait_for_clickable(self, locator):
        self.logger.info(f"Waiting for clickable of {locator}")
        return self.wait.until(
            EC.element_to_be_clickable(locator)
        )

    # ----------------------------
    # FIND MULTIPLE ELEMENTS
    # ----------------------------

    def get_elements(self, locator):
        self.logger.info(f"Getting elements from {locator}")
        return self.wait.until(
            EC.presence_of_all_elements_located(locator)
        )

    # ----------------------------
    # SCROLLING
    # ----------------------------

    def scroll_into_view(self, locator):
        """
        Ensure element becomes visible by scrolling.
        No re-centering scroll once found.
        """
        self.logger.info(f"Scrolling {locator}")
        self.scroll_until_element_visible(locator)
        time.sleep(1)
    # ----------------------------
    # DROPDOWN / AUTOSUGGEST SELECT
    # ----------------------------

    def select_from_list_by_text(self, locator, text):
        elements = self.get_elements(locator)
        self.logger.info(f"Selecting text '{text}' into {locator}")
        for el in elements:
            if text in el.text:
                el.click()
                self.logger.info(f"Clicking '{locator}'")
                time.sleep(2)
                return True
        return False

    # ----------------------------
    # VALIDATION HELPERS
    # ----------------------------

    def is_text_present_on_page(self, text):
        self.logger.info(f"Checking text '{text}' exists")
        return text in self.driver.page_source

    def is_element_present(self, locator):
        try:
            self.wait.until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def scroll_until_element_visible(self, locator, max_scrolls=10):
        """
        Scroll page gradually until element becomes visible.
        Stops immediately once found.
        """
        self.logger.info(f"Scrolling until element visible: {locator}")
        for _ in range(max_scrolls):
            try:
                element = self.wait.until(
                    EC.visibility_of_element_located(locator)
                )
                return element  # Found → stop scrolling
            except:
                self.driver.execute_script("window.scrollBy(0, 500);")
                time.sleep(1)
        self.logger.error(f"Element not found after scrolling: {locator}")
        raise Exception(f"Element not found after scrolling: {locator}")
