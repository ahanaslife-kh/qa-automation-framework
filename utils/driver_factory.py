from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import yaml



def get_driver():
    with open("config/config.yaml") as f:
        config = yaml.safe_load(f)

    options = Options()
    options.add_argument("--incognito")
    options.add_argument("--start-maximized")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.implicitly_wait(config["implicit_wait"])