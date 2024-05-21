import html

from aiogram import Bot
from aiohttp import ClientSession
from dishka import FromDishka
from loguru import logger

from common.utils.functions import get_now
from config import settings as common_settings
from .. import settings
from ..api.aiohttp import download_page
from ..api.parser import get_new_ads_list
from ..api.saver import save_page
from ..api.url import get_headers, form_url


async def check_new_notes_aiohttp(bot: FromDishka[Bot], *args, **kwargs):
    sub = ...

    async with ClientSession(headers=get_headers()) as session:
        request_url = form_url(sub.url, sub.frequency)
        now = get_now()

        page_data = await download_page(
            session=session,
            url=request_url
        )
        is_exists_new_notes = get_new_ads_list(page_data)
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
            await save_page(
                path=settings.TEMP_DIR / "pages" / filename,
                data=page_data
            )
