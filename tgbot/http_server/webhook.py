from aiogram import Bot
from loguru import logger

from config import settings


async def init_webhook(bot: Bot) -> None:
    webhook_url = f"{settings.WEBHOOK_ADDRESS}{settings.WEBHOOK_PATH}"
    await bot.set_webhook(
        url=webhook_url,
        secret_token=settings.WEBHOOK_SECRET
    )
    logger.info("SET WEBHOOK")
