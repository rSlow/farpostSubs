import html
from datetime import timedelta

from aiogram import Bot
from aiohttp import ClientSession
from loguru import logger

from common.utils.functions import get_now
from config import settings as common_settings
from .api import download_page, has_new_notes, save_page
from .url import get_headers
from .. import settings
from ..ORM.schemas import SubscriptionModel


def _form_url(sub: SubscriptionModel):
    query_dt = get_now() - timedelta(seconds=sub.frequency)
    query_ts = int(query_dt.timestamp())
    request_url = str(sub.url) + f"&date_created_min={query_ts}"
    return request_url


async def check_new_notes(sub: SubscriptionModel,
                          bot: Bot):
    async with ClientSession(headers=get_headers()) as session:
        request_url = _form_url(sub)
        now = get_now()

        page_data = await download_page(
            session=session,
            url=request_url
        )
        is_exists_new_notes = has_new_notes(page_data)
        if is_exists_new_notes:
            logger.info(f"NEW NOTE {sub.id = } {now.strftime('%d-%m-%Y %H:%M:%S')}")
            escaped_name = html.escape(sub.name)
            text = f"Для подписки <a href='{request_url}'>{escaped_name}</a> появились новые предложения!"
            await bot.send_message(
                chat_id=sub.telegram_id,
                text=text
            )

        if common_settings.DEBUG:
            filename = f"{now.strftime('%d-%m-%Y %H:%M:%S')}.html"
            save_page(
                path=settings.TEMP_DIR / "pages" / filename,
                data=page_data
            )
