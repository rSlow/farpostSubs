from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiohttp import web

from config import settings
from config.bot import bot
from config.dispatcher import dp
from config.enums import BotMode

app = web.Application()

if settings.BOT_MODE == BotMode.WEBHOOK:
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=settings.WEBHOOK_SECRET,
    )
    webhook_requests_handler.register(app, path=settings.WEBHOOK_PATH)
