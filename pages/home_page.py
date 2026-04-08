from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.ui import WebDriverWait

from selenium.common.exceptions import (

    TimeoutException,

    StaleElementReferenceException,

    ElementClickInterceptedException,

)

from pages.base_page import BasePage

from utils.logger import get_logger


class HomePage(BasePage):

    def __init__(self, driver):

        super().__init__(driver)

        self.logger = get_logger(self.__class__.__name__)

    # ---------- LOCATORS ----------

    HOTELS_TAB = (By.XPATH, "(//p[text()='Hotels'])[2]")

    CITY_INPUT = (By.XPATH, "//input[@placeholder='Enter city, area or property name']")

    FIRST_CITY = (By.CSS_SELECTOR, "div.flex.min-w-0.items-center.gap-10")

    CALENDAR_DATES = (By.CSS_SELECTOR, "button.react-calendar__tile")

    ROOM_GUEST_BTN = (By.XPATH, "//p[@data-testid='adult-increment']")

    SEARCH_BTN = ("xpath", "//button[@type='submit']")

    FROM_INPUT = (By.XPATH, "//input[contains(@placeholder,'From')]")

    TO_INPUT = (By.XPATH, "//input[contains(@placeholder,'To')]")

    # ---------- POPUP HANDLING ----------

    def remove_popup_overlay(self):

        self.logger.info("Removing popup overlay if present")

        self.driver.execute_script("""

            let backdrop = document.querySelector('.abrs-backdrop');

            if (backdrop) backdrop.remove();

            let iframe = document.querySelector('#sso-frame');

            if (iframe) iframe.remove();

        """)

    def close_popup_if_present(self):

        try:

            close_btn = WebDriverWait(self.driver, 5).until(

                EC.element_to_be_clickable(

                    (By.XPATH, "//div[@data-testid='bpg-home-modal-close']")

                )

            )

            close_btn.click()

            self.wait.until(

                EC.invisibility_of_element_located(

                    (By.XPATH, "//div[@data-testid='bpg-home-modal-close']")

                )

            )

        except:

            pass

        # Always ensure overlay is removed

        self.remove_popup_overlay()

    # ---------- HOTELS FLOW ----------

    def open_hotels(self):

        self.logger.info("Opening Hotels tab")

        self.click_element(self.HOTELS_TAB)

        self.driver.find_element(

            By.CSS_SELECTOR, ".flex-1.flex-shrink-0.text-primary.relative"

        ).click()

    def enter_city(self, city):

        self.logger.info(f"Entering city: {city}")

        city_input = self.wait_for_visibility(self.CITY_INPUT)

        city_input.clear()

        city_input.send_keys(city)

        cities = self.wait.until(

            EC.presence_of_all_elements_located(self.FIRST_CITY)

        )

        if not cities:
            raise Exception("No city suggestions appeared")

        cities[0].click()

    def select_date(self, day, month, year):

        target = f"{month} {day}, {year}"

        self.logger.info(f"Selecting date: {target}")

        dates = self.wait.until(

            EC.presence_of_all_elements_located(self.CALENDAR_DATES)

        )

        for date in dates:

            try:

                abbr = date.find_element(By.TAG_NAME, "abbr")

                aria_label = abbr.get_attribute("aria-label")

                if target in aria_label:
                    date.click()

                    return

            except:

                continue

        raise Exception(f"Date not found: {target}")

    def click_search(self):
        self.logger.info("Clicking search button")

        import time
        time.sleep(2)

        # Try multiple locators (robust approach)
        locators = [
            "//button[.//span[text()='Search']]",
            "//button[contains(.,'Search')]",
            "//div[contains(@role,'button') and contains(.,'Search')]",
            "//span[text()='Search']/ancestor::button",
            "//span[text()='Search']"
        ]

        for xpath in locators:
            try:
                elements = self.driver.find_elements("xpath", xpath)

                for el in elements:
                    if el.is_displayed():
                        self.driver.execute_script(
                            "arguments[0].scrollIntoView({block:'center'});", el
                        )
                        time.sleep(0.5)
                        self.driver.execute_script("arguments[0].click();", el)

                        self.logger.info(f"Search clicked using locator: {xpath}")
                        return

            except:
                continue

        raise Exception("Search button not found using any locator")

    def select_guests(self):

        self.logger.info("Selecting guests")

        self.wait_for_clickable(self.ROOM_GUEST_BTN).click()

    def search(self):

        self.logger.info("Clicking search")

        self.remove_popup_overlay()

        btn = self.wait_for_clickable(self.SEARCH_BTN)

        self.driver.execute_script("arguments[0].click();", btn)

    # ---------- GENERIC CITY (Reusable - Flights/Bus style) ----------

    def select_city(self, locator, city):

        self.logger.info(f"Selecting city: {city}")

        input_box = self.wait_for_visibility(locator)

        input_box.clear()

        input_box.send_keys(city)

        suggestion_locator = (By.XPATH, f"//li[contains(.,'{city}')]")

        for _ in range(3):

            try:

                suggestion = WebDriverWait(self.driver, 10).until(

                    EC.element_to_be_clickable(suggestion_locator)

                )

                suggestion.click()

                return

            except (

                    StaleElementReferenceException,

                    ElementClickInterceptedException,

                    TimeoutException,

            ):

                continue

        raise Exception("City suggestion not clickable")

    from selenium.webdriver.common.keys import Keys
    import time

    def enter_from_city(self, city):
        element = self.wait_for_visibility(self.FROM_INPUT)
        element.clear()
        element.send_keys(city)
        time.sleep(2)
        element.send_keys(Keys.ARROW_DOWN)
        element.send_keys(Keys.ENTER)

    def enter_to_city(self, city):
        element = self.wait_for_visibility(self.TO_INPUT)

        element.clear()
        element.send_keys(city)

        time.sleep(2)

        element.send_keys(Keys.ARROW_DOWN)
        element.send_keys(Keys.ENTER)

def click_search_generic(self):
    self.logger.info("Clicking search button")

    import time
    time.sleep(2)  # wait for UI validation

    btn = WebDriverWait(self.driver, 20).until(
        lambda d: d.find_element("xpath", "//button[@type='submit']")
    )

    # wait until button enabled
    WebDriverWait(self.driver, 20).until(
        lambda d: btn.is_enabled()
    )

    self.driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});", btn
    )

    self.driver.execute_script("arguments[0].click();", btn)