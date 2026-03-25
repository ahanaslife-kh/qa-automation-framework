import pytest
from pages.home_page import FlightsPage

def test_same_source_and_destination(driver):
    driver.get("https://www.ixigo.com/")
    driver.set_window_size(1920, 1080)
    flights = FlightsPage(driver)
    flights.open_flights_tab()
    flights.select_from_city("New Delhi")
    try:
        flights.enter_to_city("New Delhi")
    except Exception:
        print("Same city selection prevented by UI")
    flights.click_search()
    current_url = driver.current_url.lower()
    print("URL after invalid attempt:", current_url)
    assert "search/result" not in current_url, \
        "Search should not proceed when source and destination are same"


def test_search_without_destination(driver):
    driver.get("https://www.ixigo.com/")
    driver.set_window_size(1920, 1080)
    flights = FlightsPage(driver)
    flights.open_flights_tab()
    flights.select_from_city("New Delhi")
    flights.click_search()
    print("URL after invalid search:", driver.current_url)
    assert "search/result" not in driver.current_url.lower(), \
        "Search proceeded even without destination!"

