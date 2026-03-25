from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import time

class HomePage(BasePage):

    HOTELS_TAB = (By.XPATH, "(//p[text()='Hotels'])[2]")
    CITY_INPUT = (By.XPATH, "//input[@placeholder='Enter city, area or property name']")
    FIRST_CITY = (By.CSS_SELECTOR, "div.flex.min-w-0.items-center.gap-10")
    # CHECK_IN = (By.CLASS_NAME, ".react-calendar__tile--hasActive")
    # CHECK_OUT = (By.XPATH, "//button/abbr[@aria-label='27 February 2026']")
    CALENDAR_DATES = (By.CSS_SELECTOR, "button.react-calendar__tile")

    ROOM_GUEST_BTN = (By.XPATH, "//p[@data-testid='adult-increment']")

    SEARCH_BTN = (By.XPATH, "//div[@class='flex items-center gap-5 font-medium']")
    #POPUP_CLOSE = (By.XPATH, "//div[@data-testid='bpg-home-modal-close']")

    def open_hotels(self):
        self.driver.find_element(*self.HOTELS_TAB).click()
        self.driver.find_element(By.CSS_SELECTOR,".flex-1.flex-shrink-0.text-primary.relative").click()

    def enter_city(self, city):
         city_input = self.wait.until(
             EC.visibility_of_element_located(self.CITY_INPUT)
         )
         city_input.clear()
         city_input.send_keys(city)

         cities = self.wait.until(EC.presence_of_all_elements_located(self.FIRST_CITY))
         if not cities:
             raise Exception("No city suggestions appeared")

         cities[0].click()


#
# state=self.driver.find_elements(*self.FIRST_CITY)
# state[0].click()

    # def checkin_checkkout(self):
    #     self.wait.until(EC.element_to_be_clickable(self.CHECK_IN)).click()
    #
    #     self.wait.until(EC.element_to_be_clickable(self.CHECK_OUT)).click()

    # def checkin_checkout(self):
    #     # time.sleep(5)
    #     # date=self.driver.find_element(*self.CHECK_IN)
    #     # date.click()
    #     check=self.driver.find_element(*self.CHECK_IN)
    #     check[0].click()
    #     check[1].click()

    def select_date(self, day, month, year):
        target = f"{month} {day}, {year}"

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

    def select_guests(self):
        self.wait.until(
            EC.element_to_be_clickable(self.ROOM_GUEST_BTN)
        ).click()

    def search(self):
        self.wait.until(
            EC.element_to_be_clickable(self.SEARCH_BTN)
        ).click()

    # def close_popup(self):
    #     element = self.scroll_to_element(self.POPUP_CLOSE)
    #     self.wait.until(EC.element_to_be_clickable(self.POPUP_CLOSE))
    #     element.click()

    # def close_popup_if_present(self):
    #     try:
    #         close_btn = self.wait.until(
    #             EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='bpg-home-modal-close']"))
    #         )
    #         close_btn.click()
    #
    #         self.wait.until(
    #             EC.invisibility_of_element_located(
    #                 (By.XPATH, "//div[@data-testid='bpg-home-modal-close']")
    #             )
    #         )
    #         time.sleep(5)
    #     except:
    #         pass

    def close_popup_if_present(self):
        try:
            close_btn = self.wait.until(
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
            self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//p[contains(text(),'Couple Friendly')]")
                )
            )

        except:
            pass