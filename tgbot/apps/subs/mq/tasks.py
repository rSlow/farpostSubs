import html
from datetime import datetime
from typing import Annotated

from aiogram import Bot
from aiohttp import ClientSession

from loguru import logger
from taskiq import TaskiqDepends, Context

from common.di.utils import TASKIQ_CONTAINER_NAME
from config import settings as common_settings
from .broker import ads_broker
from .. import settings
from ..ORM.schemas import MessageSubscription
from ..api.aiohttp import download_page
from ..api.parser import get_new_ads_list, is_valid_url
from ..api.saver import save_page, DATE_FORMAT
from ..api.url import get_headers


@ads_broker.task(task_name="check_new_notes", max_retries=5)
async def check_new_notes(sub: MessageSubscription,
                          bot: Annotated[Bot, TaskiqDepends()],
                          context: Annotated[Context, TaskiqDepends()]):
    sub_time = datetime.fromtimestamp(sub.timestamp)
    str_sub_time = sub_time.strftime(DATE_FORMAT)

    request_url = str(sub.url) + f"&date_created_min={sub.timestamp}"
    headers = get_headers()
    async with ClientSession(headers=headers) as session:
        page_data = await download_page(
            session=session,
            url=request_url
        )

    is_valid = is_valid_url(page_data)

    if common_settings.DEBUG:
        filename_to_save = f"{'ERROR-' * (not is_valid)}{str_sub_time}.html"
        await save_page(
            path=settings.TEMP_DIR / "pages" / filename_to_save,
            data=page_data
        )

    if is_valid:
        new_ads_list = get_new_ads_list(page_data)
        if new_ads_list:
            logger.info(f"NEW NOTE {sub.id=} {str_sub_time}")

            escaped_name = html.escape(sub.name)
            text = f"Для подписки <a href='{request_url}'>{escaped_name}</a> появились новые предложения!"
            await bot.send_message(
                chat_id=sub.telegram_id,
                text=text
            )
    else:
        labels = context.message.labels
        if labels.get(TASKIQ_CONTAINER_NAME) is not None:
            del labels[TASKIQ_CONTAINER_NAME]
        context.reject()
