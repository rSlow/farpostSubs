import html

from config import settings as common_settings
from .. import settings
from ..api.parser import get_new_ads_list
from ..api.saver import save_page

from aiohttp import ClientSession
from ..api.aiohttp import download_page
from ..api.parser import is_valid_url
from ..api.saver import DATE_FORMAT
from ..api.url import get_headers
from ..ORM.schemas import SubscriptionModel

from faststream.rabbit import RabbitRouter
from faststream.rabbit.annotations import RabbitMessage
from loguru import logger

from common.mq.integration import AnnotatedBot
from .routing import ads_main_queue, ads_main_exchange

ads_router = RabbitRouter()


@ads_router.subscriber(
    ads_main_queue, ads_main_exchange,
    no_ack=True
)
async def check_new_ads(sub: SubscriptionModel,
                        message: RabbitMessage,
                        bot: AnnotatedBot):
    check_time = message.raw_message.timestamp.astimezone(common_settings.TIMEZONE)
    check_timestamp = check_time.timestamp()
    str_sub_time = check_time.strftime(DATE_FORMAT)

    request_url = str(sub.url) + f"&date_created_min={check_timestamp}"
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
            await message.ack()
