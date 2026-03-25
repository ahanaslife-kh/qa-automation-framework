import time
from pages.home_page import FlightsPage
from pages.search_results_page import SearchResultsPage

def test_complete_flight_booking_flow(driver,config):
    driver.get(config["base_url"])
    driver.set_window_size(1920, 1080)
    flights = FlightsPage(driver)
    flights.open_flights_tab()

    flights.select_from_city("New Delhi")
    flights.enter_to_city("Mumbai")
    flights.date_pick()
    flights.select_travel_class("Business")
    flights.click_search()

    results = SearchResultsPage(driver)
    results.wait_for_results_to_load()
    results.sort_by_cheapest()
    results.click_first_flight()
    results.wait_for_detail_panel()
    price = results.get_detail_price()
    duration = results.get_detail_duration()
    results.click_book_button()

    from selenium.webdriver.support.ui import WebDriverWait
    WebDriverWait(driver, 15).until(lambda d: "booking" in d.current_url)
    print("Navigation confirmed:", driver.current_url)
    assert price is not None, "Price not displayed on detail panel"
    assert duration is not None, "Duration not displayed on detail panel"
    time.sleep(5)
    driver.save_screenshot("screenshots/e2e_success1.png")
