import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class SearchResultsPage(BasePage):
    FLIGHT_CARD = (By.XPATH, "//div[contains(@class,'shadow-card') and contains(@class,'cursor-pointer')]")
    PRICE_ELEMENT = (By.XPATH,"//h6[@data-testid='pricing']")
    NON_STOP_FILTER = (By.XPATH,"//input[@type='checkbox' and @value='0']")
    STOP_TEXT = (By.XPATH,"//p[contains(text(),'stop') or contains(text(),'Non-stop')]")
    SORT_CHEAPEST = (By.XPATH, "//input[@type='radio' and @value='cheapest']")
    SORT_FASTEST = (By.XPATH, "//input[@type='radio' and @value='quickest']")
    SORT_BEST=(By.XPATH, "//input[@type='radio' and @value='earliest']")

    def wait_for_results_to_load(self):
        wait = WebDriverWait(self.driver, 30)
        wait.until(EC.url_contains("search"))
        wait.until(EC.presence_of_element_located(self.FLIGHT_CARD))

    def get_all_flights(self):
        return self.driver.find_elements(*self.FLIGHT_CARD)

    def get_number_of_flights(self):
        return len(self.get_all_flights())

    def get_all_airline_names(self):
        airlines = []
        elements = self.driver.find_elements(By.XPATH,"//p[contains(@class,'airlineTruncate')]")
        for i in range(len(elements)):
            try:
                elements = self.driver.find_elements(By.XPATH,"//p[contains(@class,'airlineTruncate')]")
                text = elements[i].text.strip()
                if text:
                    airlines.append(text)
            except:
                continue
        return airlines

    def get_all_prices(self):
        elements = self.driver.find_elements(*self.PRICE_ELEMENT)
        prices = []
        for el in elements:
            price_text = self.driver.execute_script("return arguments[0].innerText;", el)
            clean = price_text.replace("₹", "").replace(",", "").strip()
            prices.append(int(clean))
        return prices

    def apply_non_stop_filter(self):
        wait = WebDriverWait(self.driver, 15)
        checkbox = wait.until(EC.presence_of_element_located(self.NON_STOP_FILTER))
        self.driver.execute_script("arguments[0].click();", checkbox)
        wait.until(lambda d: True)

    def get_all_stop_texts(self):
        stops = []
        elements = self.driver.find_elements(By.XPATH,"//p[contains(text(),'stop') or contains(text(),'Non-stop')]")
        for i in range(len(elements)):
            try:
                elements = self.driver.find_elements(By.XPATH,"//p[contains(text(),'stop') or contains(text(),'Non-stop')]")
                text = elements[i].text.strip()
                if text:
                    stops.append(text)
            except:
                continue
        return stops

    def apply_airline_filter_by_code(self, airline_code):
        checkbox = self.driver.find_element(By.XPATH, f"//input[@type='checkbox' and @value='{airline_code}']")
        self.driver.execute_script("""arguments[0].scrollIntoView({behavior: 'smooth',block: 'center'});""", checkbox)
        self.driver.execute_script("arguments[0].click();", checkbox)
        time.sleep(2)

    def apply_one_stop_filter(self):
        checkbox = self.driver.find_element(By.XPATH,"//input[@type='checkbox' and @value='1']")
        self.driver.execute_script("""arguments[0].scrollIntoView({behavior: 'smooth',block: 'center'});""", checkbox)
        time.sleep(2)
        self.driver.execute_script("arguments[0].click();", checkbox)

    def reduce_max_price_slider(self, new_max):
        slider = self.driver.find_element(By.XPATH,"//input[@type='range']")
        self.driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('change'));",
                                   slider,new_max)
        self.driver.execute_script("""arguments[0].scrollIntoView({behavior: 'smooth',block: 'center'});""", slider)
        import time
        time.sleep(2)

    def reduce_duration_slider(self, hours):
            duration_section = self.driver.find_element(By.XPATH,"//p[normalize-space()='Duration']")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",duration_section)
            slider = self.driver.find_element(By.XPATH, "//p[normalize-space()='Duration']/ancestor::section//input[@type='range']")
            self.driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input')); arguments[0].dispatchEvent(new Event('change'));",slider,hours)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'shadow-card')]")))

    def get_all_durations(self):
        elements = self.driver.find_elements(By.XPATH,"//p[contains(text(),'h ') and contains(text(),'m')]")
        durations = []
        for el in elements:
            try:
                text = el.text.strip()
                parts = text.replace("m", "").split("h")
                hours = int(parts[0].strip())
                minutes = int(parts[1].strip()) if parts[1].strip() else 0
                total_hours = hours + (minutes / 60)
                durations.append(total_hours)

            except:
                continue
        return durations

    def sort_by_cheapest(self):
        radio = self.wait.until(EC.presence_of_element_located(self.SORT_CHEAPEST))
        self.driver.execute_script("arguments[0].click();", radio)
        time.sleep(2)

    def sort_by_fastest(self):
        radio = self.wait.until(EC.presence_of_element_located(self.SORT_FASTEST))
        self.driver.execute_script("arguments[0].click();", radio)
        time.sleep(2)

    def sort_by_earliest(self):
        radio = self.wait.until(EC.presence_of_element_located(self.SORT_BEST))
        self.driver.execute_script("arguments[0].click();", radio)
        time.sleep(2)

    def get_first_airline_name(self):
        airline = self.driver.find_element(By.XPATH,"(//p[contains(@class,'airlineTruncate')])[1]")
        return airline.text.strip()

    def click_first_flight(self):
        first_flight = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "(//div[contains(@class,'flex gap-5 items-center airlineInfo')])[1]")))
        first_flight.click()

    def wait_for_detail_panel(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@role='tabpanel']")))

    def get_first_card_airline_name(self):
        element = self.driver.find_element(By.XPATH,"(//p[contains(@class,'text-primary') and contains(@class,'truncate')])[1]")
        return element.text.strip()

    def get_detail_price(self):
        element = self.driver.find_element(By.XPATH,"//h4[contains(text(),'₹')]")
        return element.text.strip()

    def get_detail_duration(self):
        element = self.driver.find_element(By.XPATH,"//div[@role='tabpanel']//p[contains(text(),'2h')]")
        return element.text.strip()

    def click_book_button(self):
        WebDriverWait(self.driver, 15).until(
            lambda d: len(d.find_elements(By.XPATH, "//button[normalize-space()='Book']")) > 0
        )
        book_btn = [btn for btn in self.driver.find_elements(By.XPATH, "//button[normalize-space()='Book']")
                    if btn.is_displayed()][-1]
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", book_btn)
        book_btn.click()

    def wait_for_book_button_visible(self):
        WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.XPATH,"//button[contains(@class,'inline-flex') and normalize-space()='Book']")))
























