import asyncio
import time
import uuid
from contextlib import asynccontextmanager
from functools import wraps
from typing import ParamSpec, TypeVar, Awaitable, Callable

import aiohttp
from loguru import logger

from api import download_page, is_valid_url, save_page
from apps.subs import settings
from apps.subs.utils.url import get_headers
from common.utils.timechecker import asynctimechecker

P = ParamSpec("P")
T = TypeVar("T")


@asynccontextmanager
async def get_session():
    if settings.COOKIE_FILE.exists() and settings.COOKIE_FILE.is_file():
        loaded_jar = aiohttp.CookieJar()
        loaded_jar.load(settings.COOKIE_FILE)
    else:
        loaded_jar = None
    session = aiohttp.ClientSession(
        headers=get_headers(),
        cookie_jar=loaded_jar,
    )

    try:
        yield session
    finally:
        await session.close()
        session_jar: aiohttp.CookieJar = session.cookie_jar
        settings.COOKIE_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )
        session_jar.save(settings.COOKIE_FILE)


@asynctimechecker
async def __test__(url: str):
    async with get_session() as session:
        page_data = await download_page(session, url)
        is_valid = is_valid_url(page_data)
        if not is_valid:
            _uuid = uuid.uuid4().hex[:8]
            logger.warning(f"INVALID PAGE {_uuid}")
            await save_page(
                settings.TEMP_DIR / "pages" / f"invalid_page_{_uuid}.html",
                page_data
            )
            raise TimeoutError
        else:
            logger.info("VALID PAGE")


URL = "https://www.farpost.ru/vladivostok/realty/rent_flats/"


async def __a_main__():
    tasks = [__test__(URL) for _ in range(3)]
    await asyncio.gather(*tasks)


async def __main__():
    for _ in range(100):
        try:
            await __test__(URL)
        except TimeoutError:
            await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(__main__())
    # asyncio.run(__a_main__())
