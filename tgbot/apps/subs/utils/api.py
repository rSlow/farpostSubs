from pathlib import Path

import aiofiles
from aiohttp import ClientSession
from bs4 import BeautifulSoup


async def download_page(session: ClientSession,
                        url: str):
    await session.get("https://www.farpost.ru/")  # get cookies
    async with session.get(url) as response:
        data = await response.content.read()
    return data


async def save_page(path: Path,
                    data: bytes):
    path.parent.mkdir(parents=True, exist_ok=True)
    async with aiofiles.open(path, "wb") as file:
        await file.write(data)


def is_valid_page(data: bytes):
    soup = BeautifulSoup(data, "html.parser")
    ads_table = soup.select("table.viewdirBulletinTable")
    return bool(ads_table)


def get_new_ads_list(data: bytes):
    soup = BeautifulSoup(data, "html.parser")
    return soup.select("*[data-accuracy=sse-bulletin-new]")
