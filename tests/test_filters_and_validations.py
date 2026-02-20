from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.home_page import FlightsPage
from pages.search_results_page import SearchResultsPage
def perform_search(driver):
    driver.set_window_size(1920, 1080)
    driver.get("https://www.ixigo.com/")
    wait = WebDriverWait(driver, 15)
    flights = FlightsPage(driver)
    flights.open_flights_tab()
    wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='From']")))
    flights.select_from_city("New Delhi")
    wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='To']")))
    flights.enter_to_city("Mumbai")
    flights.date_pick()
    flights.select_travel_class("Business")
    flights.click_search()
    results = SearchResultsPage(driver)
    results.wait_for_results_to_load()
    return results

def test_non_stop_filter(driver):
    results = perform_search(driver)
    results.apply_non_stop_filter()
    stops = results.get_all_stop_texts()
    print("Stop texts:", stops)
    assert len(stops) > 0
    assert all("Non-stop" in stop for stop in stops)

def test_air_india_filter(driver):
    results = perform_search(driver)
    results.apply_airline_filter_by_code("AI")
    airlines = results.get_all_airline_names()
    assert len(airlines) > 0
    assert all("Air India" in airline for airline in airlines)

def test_indigo_filter(driver):
    results = perform_search(driver)
    results.apply_airline_filter_by_code("6E")
    airlines = results.get_all_airline_names()
    assert len(airlines) > 0
    assert all("indigo" in airline.lower() for airline in airlines)

def test_one_stop_filter(driver):
    results = perform_search(driver)
    results.apply_one_stop_filter()
    stops = results.get_all_stop_texts()
    assert len(stops) > 0
    assert all("1 stop" in stop.lower() for stop in stops)

def test_price_slider_filter(driver):
    results = perform_search(driver)
    results.reduce_max_price_slider(30000)
    prices = results.get_all_prices()
    print("Filtered prices:", prices)
    assert len(prices) > 0
    assert max(prices) <= 30000

def test_duration_filter(driver):
    results = perform_search(driver)
    results.reduce_duration_slider(5)
    durations = results.get_all_durations()
    print("Durations:", durations)
    assert len(durations) > 0
    assert max(durations) <= 5





