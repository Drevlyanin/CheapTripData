import argparse
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

EURO_SYMBOL = "\u20ac"


def set_chrome_options() -> Options:
    """Sets chrome options for Selenium.Chrome options for headless browser is enabled."""

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Min price scrapper",
        description="Get the minimal price in EUR(€) in order to get from one city to another.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("cityFrom", help="string representing a starting city")
    parser.add_argument("cityTo", help="string representing a destination city")

    args = parser.parse_args()
    if args.cityFrom == args.cityTo:
        print('[ERROR] Specify two different cities')
        exit(1)

    driver = webdriver.Chrome(options=set_chrome_options())
    url = "https://cheaptrip.guru/"
    driver.get(url)

    # city_from_input.clear()
    # city_to_input.clear()

    city_from_input = driver.find_element(By.ID, "mat-input-0")
    city_to_input = driver.find_element(By.ID, "mat-input-1")

    city_from_input.send_keys(args.cityFrom)
    time.sleep(1)  # ensure the site has time to make all necessary API calls
    city_to_input.send_keys(args.cityTo)

    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    time.sleep(1)  # ensure the site processed the request

    soup = BeautifulSoup(driver.page_source, "html.parser")
    divs = soup.find_all("div", {"class": "mat-chip-ripple"})

    prices = [float(div.next_sibling.strip().replace(EURO_SYMBOL, "")) for div in divs]
    if not prices:
        print("[ERROR] Can not recognize city name")
        driver.close()
        exit(1)

    print(f"The minimal price is: {EURO_SYMBOL}{min(prices)}")
    driver.close()
