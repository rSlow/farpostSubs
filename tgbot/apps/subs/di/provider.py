from functools import partial
from typing import Iterable

from dishka import provide, Provider, Scope
from loguru import logger
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Remote as RemoteWebDriver

from config import settings as common_settings


def get_options():
    options = Options()
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    args = ['--headless', 'window-size=1920x1080', "--disable-gpu", "--no-sandbox", "--disable-dev-shm-usage"]
    [options.add_argument(arg) for arg in args]
    return options


class A:
    ...


class B:
    ...


class DriverProvider(Provider):
    a = provide(A, scope=Scope.APP)


driver_provider = DriverProvider()
