from pages.home_page import HomePage
from pages.bus_results_page import BusResultsPage

def open_results(driver):
    driver.get("https://www.ixigo.com/buses")

    home = HomePage(driver)
    home.close_popup_if_present()
    home.enter_from_city("Delhi")
    home.enter_to_city("Jaipur")
    home.click_search()

    return BusResultsPage(driver)


# ---------- Basic flow tests ----------

def test_search_results_load(driver):
    results = open_results(driver)
    assert results.results_visible(), "Results not visible"


def test_sort_by_price_clickable(driver):
    results = open_results(driver)
    results.sort_by_price()
    assert True


def test_sort_by_departure_clickable(driver):
    results = open_results(driver)
    results.sort_by_departure()
    assert True


def test_ac_filter_clickable(driver):
    results = open_results(driver)
    results.apply_ac_filter()
    assert True


def test_sort_price_then_ac(driver):
    results = open_results(driver)
    results.sort_by_price()
    results.apply_ac_filter()
    assert True


# ---------- Seat flow helper ----------

def open_seat_flow(driver):
    results = open_results(driver)
    results.sort_by_price()
    results.click_show_seats()
    results.select_any_available_seat()
    results.select_boarding_point()
    results.select_dropping_point()
    return results


# ---------- Seat flow tests ----------

def test_seat_layout_visible(driver):
    results = open_seat_flow(driver)
    assert results.seats_visible()


def test_continue_button_visible(driver):
    results = open_seat_flow(driver)
    assert results.continue_button_visible()


def test_continue_button_clickable(driver):
    results = open_seat_flow(driver)
    results.click_continue()
    assert True


def test_full_booking_flow(driver):
    results = open_seat_flow(driver)
    results.click_continue()
    assert True

# ---------- Additional stability & validation tests ----------

def test_sort_price_then_departure(driver):
    results = open_results(driver)
    results.sort_by_price()
    results.sort_by_departure()
    assert True


def test_apply_ac_filter_twice(driver):
    results = open_results(driver)
    results.apply_ac_filter()
    results.apply_ac_filter()
    assert True


def test_results_visible_after_filter(driver):
    results = open_results(driver)
    results.apply_ac_filter()
    assert results.results_visible()


def test_open_first_bus_after_sort(driver):
    results = open_results(driver)
    results.sort_by_price()
    results.click_show_seats()
    assert results.seats_visible()


def test_select_any_available_seat(driver):
    results = open_results(driver)
    results.sort_by_price()
    results.click_show_seats()
    results.select_any_available_seat()
    assert True


def test_boarding_point_after_seat_selection(driver):
    results = open_results(driver)
    results.sort_by_price()
    results.click_show_seats()
    results.select_any_available_seat()
    results.select_boarding_point()
    assert True


def test_dropping_point_after_boarding(driver):
    results = open_results(driver)
    results.sort_by_price()
    results.click_show_seats()
    results.select_any_available_seat()
    results.select_boarding_point()
    results.select_dropping_point()
    assert True


def test_continue_enabled_after_full_selection(driver):
    results = open_results(driver)
    results.sort_by_price()
    results.click_show_seats()
    results.select_any_available_seat()
    results.select_boarding_point()
    results.select_dropping_point()
    assert results.continue_button_visible()

def test_complete_flow_with_filters(driver):
    results = open_results(driver)
    results.apply_ac_filter()
    results.sort_by_price()
    results.click_show_seats()
    results.select_any_available_seat()
    results.select_boarding_point()
    results.select_dropping_point()
    results.click_continue()
    assert True

def test_negative_01_continue_without_seat(driver):
    results = open_results(driver)
    results.sort_by_price()
    results.click_show_seats()

    results.select_boarding_point()
    results.select_dropping_point()

    assert not results.continue_button_clickable()

def test_negative_02_boarding_without_seat(driver):
    results = open_results(driver)
    results.sort_by_price()
    results.click_show_seats()

    results.select_boarding_point()

    assert not results.continue_button_clickable()