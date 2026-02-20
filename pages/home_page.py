from selenium.common import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC
class FlightsPage(BasePage):
    FLIGHTS_TAB = (By.XPATH, "//p[@class='body-sm text-xl text-primary']")
    FROM_INPUT = (By.XPATH, "//span[text()='From']")
    TO_INPUT = (By.XPATH, "//span[text()='To']/ancestor::div[1]")
    DATE_PICK=(By.XPATH, "//p[@data-testid='departureDate']")
    SEARCH_BUTTON = (By.XPATH, "//button[normalize-space()='Search']")
    def open_flights_tab(self):
        self.click(self.FLIGHTS_TAB)
    def select_from_city(self, city):
        self.click(self.FROM_INPUT)
        active_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input")))
        active_input.clear()
        active_input.send_keys(city)
        for _ in range(5):
            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, f"//span[contains(@class,'block truncate') and contains(.,'{city}')]")))
                self.driver.find_element(By.XPATH,f"(//span[contains(@class,'block truncate') and contains(.,'{city}')])[1]").click()
                break
            except StaleElementReferenceException:
                continue
        self.driver.find_element(By.TAG_NAME, "body").click()
        WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located( (By.XPATH, "//div[contains(@class,'overflow-y-scroll')]")))

    def enter_to_city(self, city):
        to_label = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()='To']")))
        self.driver.execute_script("arguments[0].click();", to_label)
        WebDriverWait(self.driver, 10).until(lambda d: d.execute_script("return document.activeElement.tagName") == "INPUT")
        active_input = self.driver.switch_to.active_element
        active_input.clear()
        active_input.send_keys(city)
        option_xpath = f"(//div[contains(@class,'overflow-y-scroll')]//span[contains(normalize-space(),'{city}')])[1]"
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, option_xpath))).click()
        self.driver.find_element(By.TAG_NAME, "body").click()
        WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located((By.XPATH, "//div[contains(@class,'overflow-y-scroll')]")))

    def date_pick(self):
        wait = WebDriverWait(self.driver, 15)
        self.click(self.DATE_PICK)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class,'react-calendar')]")))
        date = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'react-calendar')]//abbr[text()='22']")))
        date.click()
        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        wait.until(EC.invisibility_of_element_located((By.XPATH, "//div[contains(@class,'react-calendar')]")))

    def select_travel_class(self, travel_class):
        wait = WebDriverWait(self.driver, 15)
        pax = wait.until(EC.element_to_be_clickable((By.XPATH, "//p[@data-testid='pax']")))
        pax.click()
        option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[normalize-space()='{travel_class}']")))
        option.click()
        done_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Done']")))
        done_btn.click()

    def wait_for_results_to_load(self):
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class,'flight-card')]")))

    def click_search(self):
        wait = WebDriverWait(self.driver, 20)
        search_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Search')]")))
        self.driver.execute_script("""arguments[0].scrollIntoView({block: 'center'});""", search_btn)
        wait.until(lambda d: search_btn.is_displayed())
        search_btn.click()




