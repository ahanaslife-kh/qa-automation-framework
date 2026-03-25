import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.home_page import FlightsPage
from pages.search_results_page import SearchResultsPage
def test_flight_search(driver):
    driver.set_window_size(1920, 1080)
    driver.get("https://www.ixigo.com/")
    wait = WebDriverWait(driver, 15)
    flights = FlightsPage(driver)
    flights.open_flights_tab()
    wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='From']")))
    flights.select_from_city("New Delhi")
    wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='To']")))
    flights.enter_to_city("Mumbai")
    driver.find_element(By.TAG_NAME, "body").click()
    flights.date_pick()
    flights.select_travel_class("Business")
    flights.click_search()
    wait.until(EC.url_contains("search"))
    print("Current URL:", driver.current_url)
    results=SearchResultsPage(driver)
    results.wait_for_results_to_load()
    count = results.get_number_of_flights()
    print("Flights found:", count)
    assert count > 0
    prices = results.get_all_prices()
    print("Extracted Prices:", prices)
    assert len(prices) > 0
    assert all(price > 0 for price in prices)













