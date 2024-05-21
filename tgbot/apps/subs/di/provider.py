from typing import AsyncIterable

from dishka import provide, Provider, Scope
from loguru import logger
from selenium.webdriver import Remote as RemoteWebDriver
from selenium.webdriver.chrome.options import Options

from common.utils.decorators import to_async_thread
from config import settings as common_settings


class AdsProvider(Provider):
    component = "ads"

    @provide(scope=Scope.APP)
    async def get_webdriver(self) -> AsyncIterable[RemoteWebDriver]:
        logger.info("create webdriver")
        options = Options()
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        args = ['--headless', 'window-size=1920x1080', "--disable-gpu", "--no-sandbox", "--disable-dev-shm-usage"]
        [options.add_argument(arg) for arg in args]

        webdriver = RemoteWebDriver(
            common_settings.SELENIUM_URL,
            options=options
        )
        logger.info(f"{id(webdriver)=}")
        yield webdriver
        logger.info("webdriver is closing")
        await to_async_thread(webdriver.close)()
