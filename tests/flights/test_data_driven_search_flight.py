import json
import pytest
from pages.home_page import FlightsPage
from pages.search_results_page import SearchResultsPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def load_test_data():
    with open("data/test_data.json") as f:
        return json.load(f)

@pytest.mark.parametrize("data", load_test_data())
def test_flight_search_data_driven(driver, data):
    driver.get("https://www.ixigo.com/")
    driver.set_window_size(1920, 1080)
    flights = FlightsPage(driver)
    flights.open_flights_tab()
    flights.select_from_city(data["from_city"])
    flights.enter_to_city(data["to_city"])
    flights.date_pick()
    flights.select_travel_class(data["travel_class"])
    flights.click_search()
    wait = WebDriverWait(driver, 20)
    wait.until(EC.url_contains("search"))
    results = SearchResultsPage(driver)
    results.wait_for_results_to_load()
    prices = results.get_all_prices()
    assert len(prices) > 0, f"No flights found for {data}"
