import time
from selenium.common import StaleElementReferenceException, ElementClickInterceptedException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import get_logger


class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        self.logger = get_logger(self.__class__.__name__)

    # ---------- CLICK ----------

    def click_element(self, locator):
        for attempt in range(3):
            try:
                element = self.wait.until(EC.element_to_be_clickable(locator))

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", element
                )

                self.logger.info(f"Clicking element: {locator}")

                try:
                    element.click()
                except ElementClickInterceptedException:
                    self.logger.warning("Using JS click fallback")
                    self.driver.execute_script("arguments[0].click();", element)

                return

            except StaleElementReferenceException:
                self.logger.warning("Retrying click due to stale element...")
                time.sleep(1)

        raise Exception(f"Unable to click element: {locator}")

    # ---------- INPUT ----------

    def enter_text(self, locator, value):
        for attempt in range(3):
            try:
                element = self.wait.until(EC.visibility_of_element_located(locator))
                self.logger.info(f"Entering text '{value}' into {locator}")
                element.clear()
                element.send_keys(value)
                return

            except StaleElementReferenceException:
                self.logger.warning("Retrying send_keys...")
                time.sleep(1)

        raise Exception(f"Unable to enter text: {locator}")

    # ---------- WAITS ----------

    def wait_for_element(self, locator):
        self.logger.info(f"Waiting for visibility: {locator}")
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_for_presence(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def wait_for_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    # ---------- GETTERS ----------

    def get_text(self, locator):
        return self.wait_for_element(locator).text

    def get_elements(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    # ---------- VALIDATIONS ----------

    def is_visible(self, locator):
        self.wait_for_element(locator)
        return True

    def is_element_present(self, locator):
        try:
            self.wait_for_presence(locator)
            return True
        except TimeoutException:
            return False

    def is_text_present_on_page(self, text):
        return text in self.driver.page_source

    @staticmethod
    def validate_text(actual, expected):
        logger = get_logger()
        logger.info(f"Validating text. Expected: {expected} | Actual: {actual}")
        assert expected in actual, f"Expected '{expected}' not found in '{actual}'"

    # ---------- SCROLL ----------

    def scroll_to_element(self, locator):
        element = self.wait_for_element(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )
        return element

    def scroll_until_element_visible(self, locator, max_scrolls=10):
        for _ in range(max_scrolls):
            try:
                return self.wait_for_element(locator)
            except:
                self.driver.execute_script("window.scrollBy(0, 500);")
                time.sleep(1)

        raise Exception(f"Element not found after scrolling: {locator}")

    # ---------- UTILITIES ----------

    def js_click(self, locator):
        self.logger.warning(f"Using JS click for: {locator}")
        element = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].click();", element)

    def switch_to_new_tab(self):
        self.wait.until(lambda d: len(d.window_handles) > 1)
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def select_from_list_by_text(self, locator, text):
        elements = self.get_elements(locator)

        for el in elements:
            if text in el.text:
                el.click()
                return True

        return False