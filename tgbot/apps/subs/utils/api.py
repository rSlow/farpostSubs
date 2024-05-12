from pathlib import Path

from aiohttp import ClientSession
from bs4 import BeautifulSoup


async def download_page(session: ClientSession,
                        url: str):
    await session.get("https://www.farpost.ru/")  # get cookies
    async with session.get(url) as response:
        data = await response.content.read()
    return data


def save_page(path: Path,
              data: bytes):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as file:
        file.write(data)


def is_valid_url(data: bytes):
    soup = BeautifulSoup(data, "html.parser")
    ads_table = soup.select("table.viewdirBulletinTable")
    return bool(ads_table)


def has_new_notes(data: bytes):
    soup = BeautifulSoup(data, "html.parser")
    new_ads = soup.select("*[data-accuracy=sse-bulletin-new]")
    return bool(new_ads)
