import time
from selenium.common import StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def click(self, locator):
        for attempt in range(3):
            try:
                element = self.wait.until(EC.presence_of_element_located(locator))
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",element)
                self.wait.until(EC.element_to_be_clickable(locator))
                try:
                    element.click()
                except ElementClickInterceptedException:
                    print("Normal click failed, using JS click fallback")
                    self.driver.execute_script("arguments[0].click();",element)
                return
            except StaleElementReferenceException:
                print("Retrying click due to stale element...")
                time.sleep(1)
        raise Exception(f"Unable to click element after retries: {locator}")

    def type(self, locator, text):
        for attempt in range(3):
            try:
                element = self.wait.until( EC.visibility_of_element_located(locator))
                element.clear()
                element.send_keys(text)
                return
            except StaleElementReferenceException:
                print("Retrying send_keys due to stale element...")
                time.sleep(1)
        raise Exception(f"Unable to enter text after retries: {locator}")

    def wait_for(self, locator):
        return self.wait.until( EC.visibility_of_element_located(locator))
