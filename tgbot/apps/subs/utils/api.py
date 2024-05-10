import os
from datetime import timedelta
from pathlib import Path

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from .. import settings
from common.utils.functions import get_now
from ..ORM.schemas import SubscriptionModel


def get_headers():
    return {
        "Accept": "text/html,"
                  "application/xhtml+xml,"
                  "application/xml;q=0.9,"
                  "image/avif,"
                  "image/webp,"
                  "image/apng,"
                  "*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "ru-RU,ru;q=0.9",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": UserAgent().random
    }


def form_url(sub: SubscriptionModel):
    now = get_now() - timedelta(seconds=sub.frequency)
    now_ts = int(now.timestamp())
    request_url = str(sub.url) + f"?since={now_ts}"
    return request_url


async def download_page(session: ClientSession,
                        url: str):
    async with session.get(url) as response:
        data = await response.content.read()
    return data


def save_page(path: Path,
              data: bytes):
    if not settings.TEMP_DIR.exists():
        os.mkdir(settings.TEMP_DIR)
    with open(path, "wb") as file:
        file.write(data)


def has_new_notes(data: bytes):
    soup = BeautifulSoup(data, "html.parser")
    new_elements = soup.select("*[data-accuracy=sse-bulletin-new]")
    return bool(new_elements)
