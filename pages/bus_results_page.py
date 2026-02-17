from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BusResultsPage(BasePage):

    RESULT_TEXT = (By.XPATH, "//span[contains(text(),'Showing')]")

    SORT_DEPARTURE = (By.XPATH, "//span[text()='Departure Time']")

    # Sort
    SORT_PRICE = (By.XPATH, "//span[text()='Price']")

    # Filters
    AC_FILTER = (By.XPATH, "//span[text()='AC']")

    FIRST_SHOW_SEATS = (
        By.XPATH,
        "(//button[contains(.,'Show Seats')])[1]"
    )

    # Seat container
    AVAILABLE_SEATS = (
        By.XPATH,
        "//button[contains(@class,'seat') and not(contains(@class,'booked'))]"
    )

    # Boarding & Dropping lists
    BOARDING_OPTIONS = (
        By.XPATH,
        "//div[contains(@id,'place-container')]//input[@type='checkbox']"
    )

    DROPPING_OPTIONS = (
        By.XPATH,
        "//div[contains(@id,'place-container')]//input[@type='checkbox']"
    )

    CONTINUE_BTN = (
        By.XPATH,
        "//button[contains(.,'Continue')]"
    )

    # Seat container (used for validation)
    SEAT_CONTAINER = (By.XPATH, "//button[contains(@class,'seat')]")

    def results_visible(self):
        try:
            WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located(self.RESULT_TEXT)
            )
            return True
        except:
            return False

    def sort_by_price(self):
        self.click_element(self.SORT_PRICE)

    def apply_ac_filter(self):
        self.click_element(self.AC_FILTER)

    def click_show_seats(self):
        btn = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(self.FIRST_SHOW_SEATS)
        )
        self.driver.execute_script("arguments[0].click();", btn)

    def select_any_available_seat(self):
        seats = WebDriverWait(self.driver, 30).until(
            EC.presence_of_all_elements_located(self.AVAILABLE_SEATS)
        )

        for seat in seats:
            try:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", seat)
                WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable(seat)
                )
                self.driver.execute_script("arguments[0].click();", seat)
                break
            except:
                continue

    def select_boarding_point(self):
        options = WebDriverWait(self.driver, 30).until(
            EC.presence_of_all_elements_located(self.BOARDING_OPTIONS)
        )

        for opt in options:
            try:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", opt)
                WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable(opt)
                )
                self.driver.execute_script("arguments[0].click();", opt)
                break
            except:
                continue

    def select_dropping_point(self):
        options = WebDriverWait(self.driver, 30).until(
            EC.presence_of_all_elements_located(self.DROPPING_OPTIONS)
        )

        for opt in options:
            try:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", opt)
                WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable(opt)
                )
                self.driver.execute_script("arguments[0].click();", opt)
                break
            except:
                continue

    def click_continue(self):
        btn = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located(self.CONTINUE_BTN)
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)

        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.CONTINUE_BTN)
        )

        self.driver.execute_script("arguments[0].click();", btn)

    def continue_button_visible(self):
        try:
            WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located(self.CONTINUE_BTN)
            )
            return True
        except:
            return False

    def sort_by_departure(self):
        self.click_element(self.SORT_DEPARTURE)

    # def apply_sleeper_filter(self):
    #     self.click_element(self.SLEEPER_FILTER)

    def seats_visible(self):
        try:
            self.wait_for_visibility(self.SEAT_CONTAINER, timeout=20)
            return True
        except:
            return False
