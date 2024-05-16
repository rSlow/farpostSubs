from contextlib import contextmanager
from functools import partial

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from common.utils.decorators import to_async_thread
from config import settings


@contextmanager
def selenium_driver():
    options = webdriver.ChromeOptions()
    args = [
        '--headless',
        'window-size=1920x1080',
        # "--disable-gpu",
        "--no-sandbox",
        "--disable-dev-shm-usage"
    ]
    [options.add_argument(arg) for arg in args]
    driver = webdriver.Remote(
        settings.SELENIUM_URL,
        DesiredCapabilities.CHROME,
        options=options
    )

    try:
        yield driver
    finally:
        driver.close()
        driver.quit()


@to_async_thread
def has_new_ads(url: str):
    with selenium_driver() as driver:
        driver.get(url)
        driver.implicitly_wait(10)
        new_ads = driver.find_elements("*[data-accuracy=sse-bulletin-new]", By.CSS_SELECTOR)
        return new_ads


@to_async_thread
def is_valid_url(url: str):
    with selenium_driver() as driver:
        driver.get(url)
        driver.implicitly_wait(10)
        ads_table = driver.find_element("table.viewdirBulletinTable", By.CSS_SELECTOR)
        return ads_table
