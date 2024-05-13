import html
from datetime import datetime

from aiohttp import ClientSession
from loguru import logger

from common.mq.exceptions import RejectedError
from config import settings as common_settings
from config.bot import bot
from .functions import as_strftime
from .. import settings
from ..ORM.schemas import MessageSubscription
from ..utils.api import download_page, has_new_notes, save_page, is_valid_page
from ..utils.url import get_headers


def __form_request_url(sub: MessageSubscription):
    return str(sub.url) + f"&date_created_min={sub.timestamp}"


async def check_new_ads(sub: MessageSubscription):
    sub_dt = datetime.fromtimestamp(sub.timestamp, common_settings.TIMEZONE)

    async with ClientSession(headers=get_headers()) as session:
        request_url = __form_request_url(sub)
        page_data = await download_page(
            session=session,
            url=request_url
        )

    is_valid = is_valid_page(page_data)
    if not is_valid:
        if common_settings.DEBUG:
            filename = f"ERROR {as_strftime(sub_dt)}.html"
            save_page(
                path=settings.TEMP_DIR / "pages" / filename,
                data=page_data
            )
        raise RejectedError(f"page at task {as_strftime(sub_dt)} is not valid")

    is_exists_new_notes = has_new_notes(page_data)
    if is_exists_new_notes:
        logger.info(f"NEW NOTE {sub.id=} {as_strftime(sub_dt)}")
        escaped_name = html.escape(sub.name)
        text = f"Для подписки <a href='{request_url}'>{escaped_name}</a> появились новые предложения!"
        await bot.send_message(
            chat_id=sub.telegram_id,
            text=text
        )

    if common_settings.DEBUG:
        filename = f"{as_strftime(sub_dt)}.html"
        save_page(
            path=settings.TEMP_DIR / "pages" / filename,
            data=page_data
        )
