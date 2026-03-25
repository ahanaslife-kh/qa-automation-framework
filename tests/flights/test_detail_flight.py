import time
from tests.test_filters_and_validations import perform_search
def test_sort_by_cheapest(driver):
    results = perform_search(driver)
    results.sort_by_cheapest()
    prices = results.get_all_prices()
    assert prices == sorted(prices), "Prices not sorted Low → High"

def test_sort_by_fastest(driver):
    results = perform_search(driver)
    results.sort_by_fastest()
    results.get_all_durations()
    assert False

def test_sort_by_earliest(driver):
    results = perform_search(driver)
    results.sort_by_earliest()
    results.get_all_durations()
    assert False

def test_detail_airline_name_matches(driver):
    results = perform_search(driver)
    card_name = results.get_first_card_airline_name()
    results.click_first_flight()
    results.wait_for_detail_panel()
    detail_name = results.get_first_card_airline_name()
    print("Card:", card_name)
    print("Detail:", detail_name)
    assert card_name.split("|")[0].strip() in detail_name

def test_detail_price_present(driver):
    results = perform_search(driver)
    results.click_first_flight()
    results.wait_for_detail_panel()
    price = results.get_detail_price()
    print("Detail Price:", price)
    assert "₹" in price

def test_detail_duration_present(driver):
    results = perform_search(driver)
    results.click_first_flight()
    results.wait_for_detail_panel()
    duration = results.get_detail_duration()
    print("Detail Duration:", duration)
    assert "h" in duration

def test_click_book_button(driver):
    results = perform_search(driver)
    results.click_first_flight()
    results.wait_for_detail_panel()
    results.click_book_button()
    time.sleep(3)
    print("URL after click:", driver.current_url)







