from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import get_logger
logger = get_logger()
from utils.wait_utils import wait_for_visibility, wait_for_clickable
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class HomePage(BasePage):

    FROM_INPUT = (By.XPATH, "//input[contains(@placeholder,'From')]")
    TO_INPUT = (By.XPATH, "//input[contains(@placeholder,'To')]")
    SEARCH_BTN = (By.XPATH, "//button[contains(.,'Search')]")

    def remove_popup_overlay(self):
        """Force remove any login overlay"""
        self.driver.execute_script("""
            let backdrop = document.querySelector('.abrs-backdrop');
            if (backdrop) backdrop.remove();

            let iframe = document.querySelector('#sso-frame');
            if (iframe) iframe.remove();
        """)

    def select_city(self, locator, city):
        input_box = self.wait_for_visibility(locator)
        input_box.clear()
        input_box.send_keys(city)

        suggestion_locator = (By.XPATH, f"//li[contains(.,'{city}')]")

        for _ in range(3):  # retry logic without sleep
            try:
                suggestion = wait_for_clickable(self.driver, suggestion_locator, timeout=10)
                suggestion.click()
                return
            except (StaleElementReferenceException, ElementClickInterceptedException, TimeoutException):
                # retry automatically without sleep
                continue

        raise Exception("City suggestion not clickable")

    def close_login_popup_if_present(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.frame_to_be_available_and_switch_to_it((By.ID, "sso-frame"))
            )

            close_btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'close')]"))
            )
            close_btn.click()

            self.driver.switch_to.default_content()
        except:
            self.driver.switch_to.default_content()

        # Always remove overlay
        self.remove_popup_overlay()

    def enter_from_city(self, city):
        self.select_city(self.FROM_INPUT, city)

    def enter_to_city(self, city):
        self.select_city(self.TO_INPUT, city)

    def click_search(self):
        self.remove_popup_overlay()
        btn = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(self.SEARCH_BTN)
        )
        self.driver.execute_script("arguments[0].click();", btn)
