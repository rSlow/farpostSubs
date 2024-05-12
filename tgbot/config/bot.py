from aiogram import Bot

from . import settings

bot = Bot(
    token=settings.BOT_TOKEN,
    parse_mode="HTML"
)
