import asyncio
import uuid

from dishka import make_container, Scope
from loguru import logger

from apps.subs import settings
from apps.subs.di.provider import driver_provider, A, B
from apps.subs.utils.api import is_valid_url
from common.utils.decorators import to_async_thread
from common.utils.timechecker import timechecker

from selenium.webdriver import Remote as RemoteWebdriver


@to_async_thread
@timechecker
def __test__(url: str, ):
    logger.info("start __test__")

    container = make_container(driver_provider, start_scope=Scope.RUNTIME)
    a = container.get(A)

    print(repr(a))
    # driver.get(url)
    # driver.implicitly_wait(10)
    # page_data = driver.page_source
    #
    # is_valid = is_valid_url(page_data)
    # if not is_valid:
    #     _uuid = uuid.uuid4().hex[:8]
    #     logger.warning(f"INVALID PAGE {_uuid}")
    #     with open(settings.TEMP_DIR / "pages" / f"invalid_page_{_uuid}.html", "w") as file:
    #         file.write(page_data)
    # else:
    #     logger.info("VALID PAGE")


async def __a_main__(times: int):
    tasks = [__test__(URL) for _ in range(times)]
    await asyncio.gather(*tasks)


async def __main__():
    for _ in range(5):
        await __test__(URL)


URL = "https://www.farpost.ru/vladivostok/realty/rent_flats/"

if __name__ == '__main__':
    logger.info("START")

    asyncio.run(__main__())
    # asyncio.run(__a_main__(3))
