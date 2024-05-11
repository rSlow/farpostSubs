import html

from aiogram import Bot
from aiohttp import ClientSession
from loguru import logger

from common.utils.functions import get_now
from config import settings as common_settings
from .api import get_headers, download_page, has_new_notes, form_url, save_page
from .. import settings
from ..ORM.schemas import SubscriptionModel


async def check_new_notes(sub: SubscriptionModel,
                          bot: Bot):
    async with ClientSession(headers=get_headers()) as session:
        request_url = form_url(sub)
        page_data = await download_page(
            session=session,
            url=request_url
        )

        now = get_now()
        filename = f"{now.strftime('%d-%m-%Y %H:%M:%S')}.html"
        if common_settings.DEBUG:
            save_page(
                path=settings.TEMP_DIR / "pages" / filename,
                data=page_data
            )

        is_exists_new_notes = has_new_notes(page_data)
        if is_exists_new_notes:
            logger.info(f"NEW NOTE {sub.id = } {now.strftime('%d-%m-%Y %H:%M:%S')}")
            escaped_name = html.escape(sub.name)
            text = f"Для подписки <a href='{sub.url}'>{escaped_name}</a> появились новые предложения!"
            await bot.send_message(
                chat_id=sub.telegram_id,
                text=text
            )
