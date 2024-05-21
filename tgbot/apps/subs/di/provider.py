from typing import AsyncIterable, Annotated

from dishka import provide, Provider, Scope, FromComponent
from loguru import logger
from selenium.webdriver import Remote as RemoteWebDriver
from selenium.webdriver.chrome.options import Options
from sqlalchemy.ext.asyncio import AsyncSession
from taskiq_aio_pika import AioPikaBroker

from common.utils.decorators import to_async_thread
from config import settings as common_settings, settings
from ..scheduler import AdsScheduler


class AdsProvider(Provider):
    component = "ads"
    scope = Scope.APP

    @provide
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

    @provide
    async def get_broker(self) -> AsyncIterable[AioPikaBroker]:
        logger.info("create broker")
        broker = AioPikaBroker(
            url=settings.RABBITMQ_URL,
            exchange_name="ads",
            queue_name="ads",
        )
        await broker.startup()
        logger.info(f"{id(broker)=}")
        yield broker
        logger.info("broker is closing")
        await broker.shutdown()

    @provide
    async def get_scheduler(self,
                            broker: AioPikaBroker,
                            session: Annotated[AsyncSession, FromComponent("sql")]) -> AdsScheduler:
        logger.info("create scheduler")
        scheduler = AdsScheduler(
            broker=broker,
        )
        await scheduler.init(session)
        logger.info(f"{id(scheduler)=}")
        return scheduler
