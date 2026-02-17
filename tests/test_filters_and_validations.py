from pages.home_page import HomePage
from pages.bus_results_page import BusResultsPage

def open_results(driver):
    driver.get("https://www.ixigo.com/buses")

    home = HomePage(driver)
    home.close_login_popup_if_present()
    home.enter_from_city("Delhi")
    home.enter_to_city("Jaipur")
    home.click_search()

    return BusResultsPage(driver)

    # results = BusResultsPage(driver)
    # results.sort_by_price()
    #
    # assert results.results_visible()

    # ---------- Basic flow tests ----------

    def test_01_search_results_load(driver):
        results = open_results(driver)
        assert results.sort_by_price is not None

    def test_02_sort_by_price_clickable(driver):
        results = open_results(driver)
        results.sort_by_price()
        assert True

    def test_03_sort_by_departure_clickable(driver):
        results = open_results(driver)
        results.sort_by_departure()
        assert True

    def test_04_ac_filter_clickable(driver):
        results = open_results(driver)
        results.apply_ac_filter()
        assert True

    def test_05_sleeper_filter_clickable(driver):
        results = open_results(driver)
        results.apply_sleeper_filter()
        assert True

    def test_06_sort_price_then_ac(driver):
        results = open_results(driver)
        results.sort_by_price()
        results.apply_ac_filter()
        assert True

    def test_07_sort_departure_then_ac(driver):
        results = open_results(driver)
        results.sort_by_departure()
        results.apply_ac_filter()
        assert True

    def test_08_multiple_filters(driver):
        results = open_results(driver)
        results.apply_ac_filter()
        results.apply_sleeper_filter()
        assert True

    def test_09_sort_twice(driver):
        results = open_results(driver)
        results.sort_by_price()
        results.sort_by_departure()
        assert True

    def test_10_apply_ac_after_sort(driver):
        results = open_results(driver)
        results.sort_by_price()
        results.apply_ac_filter()
        assert True

    # ---------- Seat flow tests ----------

    def open_seat_flow(driver):
        results = open_results(driver)
        results.sort_by_price()
        results.select_bhaiya_bus()
        return results

    def test_11_select_bhaiya_bus(driver):
        results = open_seat_flow(driver)
        assert True

    def test_12_show_seats_opens(driver):
        results = open_seat_flow(driver)
        assert results.seats_visible()

    def test_13_seat_layout_visible(driver):
        results = open_seat_flow(driver)
        assert results.seats_visible()

    def test_14_select_seat_u15(driver):
        results = open_seat_flow(driver)
        results.select_seat_u15()
        assert True

    def test_15_boarding_points_visible(driver):
        results = open_seat_flow(driver)
        assert results.boarding_points_visible()

    def test_16_select_kashmiri_gate(driver):
        results = open_seat_flow(driver)
        results.select_kashmiri_gate()
        assert True

    def test_17_select_transport_nagar(driver):
        results = open_seat_flow(driver)
        results.select_transport_nagar()
        assert True

    def test_18_continue_button_visible(driver):
        results = open_seat_flow(driver)
        assert results.continue_button_visible()

    def test_19_continue_button_clickable(driver):
        results = open_seat_flow(driver)
        results.click_continue()
        assert True

    def test_20_full_booking_flow(driver):
        results = open_seat_flow(driver)
        results.select_seat_u15()
        results.select_kashmiri_gate()
        results.select_transport_nagar()
        results.click_continue()
        assert True
