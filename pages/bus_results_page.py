from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BusResultsPage(BasePage):

    RESULT_TEXT = (By.XPATH, "//button[contains(.,'Show Seats')]")

    SORT_DEPARTURE = (By.XPATH, "//span[text()='Departure Time']")

    # Sort
    SORT_PRICE = (By.XPATH, "//span[contains(text(),'Price')]")

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
            WebDriverWait(self.driver, 30).until(
                lambda d: (
                        len(d.find_elements(By.XPATH, "//button[contains(.,'Seats')]")) > 0
                        or len(d.find_elements(By.XPATH, "//div[contains(@class,'bus')]")) > 0
                )
            )
            return True
        except:
            return False

    def sort_by_price(self):
        self.logger.info("Sorting by price")

        btn = self.wait_for_clickable(self.SORT_PRICE)
        self.driver.execute_script("arguments[0].click();", btn)

    def apply_ac_filter(self):
        self.click_element(self.AC_FILTER)

        # wait for results refresh
        WebDriverWait(self.driver, 20).until(
            lambda d: len(
                d.find_elements(By.XPATH, "//button[contains(.,'Seats')]")
            ) > 0
        )

    def click_show_seats(self):
        self.logger.info("Clicking show seats")

        import time
        time.sleep(3)  # allow results to fully load

        locators = [
            "//button[contains(.,'Seats')]",
            "//span[contains(.,'Seats')]",
            "//div[contains(.,'Seats')]",
        ]

        for xpath in locators:
            try:
                elements = self.driver.find_elements("xpath", xpath)

                for el in elements:
                    try:
                        if el.is_displayed():
                            self.driver.execute_script(
                                "arguments[0].scrollIntoView({block:'center'});", el
                            )
                            time.sleep(0.5)
                            self.driver.execute_script("arguments[0].click();", el)

                            self.logger.info(f"Clicked seats using {xpath}")

                            # ✅ WAIT FOR SEAT LAYOUT
                            WebDriverWait(self.driver, 20).until(
                                lambda d: len(
                                    d.find_elements("xpath", "//*[contains(@class,'seat')]")
                                ) > 0
                            )

                            return
                    except:
                        continue

            except:
                continue

        raise Exception("No seat button found")

    def select_any_available_seat(self):
        for i in range(5):
            try:
                seats = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_all_elements_located(self.AVAILABLE_SEATS)
                )

                if len(seats) == 0:
                    continue

                seat = seats[0]  #  ONLY FIRST SEAT

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});", seat
                )

                WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable(seat)
                )

                self.driver.execute_script("arguments[0].click();", seat)

                print(" Seat selected")
                return

            except Exception as e:
                print(f"Retry seat selection {i + 1}: {e}")

        raise Exception(" Seat not selected")

    def continue_button_clickable(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.CONTINUE_BTN)
            )
            return True
        except:
            return False

    def select_boarding_point(self):
        self.logger.info("Selecting boarding point")

        import time
        time.sleep(2)

        # Try multiple locator strategies
        locators = [
            "//div[contains(text(),'Boarding')]",
            "//span[contains(text(),'Boarding')]",
            "//div[contains(@class,'boarding')]",
        ]

        for xpath in locators:
            try:
                elements = self.driver.find_elements("xpath", xpath)

                for el in elements:
                    try:
                        if el.is_displayed():
                            self.driver.execute_script(
                                "arguments[0].scrollIntoView({block:'center'});", el
                            )
                            time.sleep(0.5)
                            self.driver.execute_script("arguments[0].click();", el)

                            self.logger.info(f"Boarding selected using {xpath}")
                            return
                    except:
                        continue

            except:
                continue

        self.logger.warning("Boarding not required or auto-selected")

    def select_dropping_point(self):
        self.logger.info("Selecting dropping point")

        import time
        time.sleep(2)

        locators = [
            "//div[contains(text(),'Dropping')]",
            "//span[contains(text(),'Dropping')]",
            "//div[contains(@class,'dropping')]",
        ]

        for xpath in locators:
            try:
                elements = self.driver.find_elements("xpath", xpath)

                for el in elements:
                    try:
                        if el.is_displayed():
                            self.driver.execute_script(
                                "arguments[0].scrollIntoView({block:'center'});", el
                            )
                            time.sleep(0.5)
                            self.driver.execute_script("arguments[0].click();", el)

                            self.logger.info(f"Dropping selected using {xpath}")
                            return
                    except:
                        continue

            except:
                continue

        self.logger.warning("Dropping not required or auto-selected")

    def click_continue(self):
        self.logger.info("Clicking continue button")

        import time
        time.sleep(2)

        locators = [
            "//button[contains(.,'Continue')]",
            "//span[contains(.,'Continue')]",
            "//button[contains(.,'Proceed')]",
            "//span[contains(.,'Proceed')]",
        ]

        for xpath in locators:
            try:
                elements = self.driver.find_elements("xpath", xpath)

                for el in elements:
                    if el.is_displayed():
                        self.driver.execute_script(
                            "arguments[0].scrollIntoView({block:'center'});", el
                        )
                        self.driver.execute_script("arguments[0].click();", el)
                        return
            except:
                continue

        raise Exception("Continue button not found")

    def continue_button_visible(self):
        import time
        time.sleep(2)

        locators = [
            "//button[contains(.,'Continue')]",
            "//span[contains(.,'Continue')]",
            "//button[contains(.,'Proceed')]",
            "//span[contains(.,'Proceed')]",
        ]

        for xpath in locators:
            try:
                elements = self.driver.find_elements("xpath", xpath)

                for el in elements:
                    if el.is_displayed():
                        return True
            except:
                continue

        return False

    def sort_by_departure(self):
        self.click_element(self.SORT_DEPARTURE)

    def seats_visible(self):
        return len(
            self.driver.find_elements("xpath", "//*[contains(@class,'seat')]")
        ) > 0
