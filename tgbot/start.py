from aiogram.webhook.aiohttp_server import setup_application as setup
from aiohttp.web import run_app

from config import settings
from config.bot import bot
from config.dispatcher import dp, init_dispatcher
from config.enums import BotMode
from http_server.app import app as http_app

if __name__ == '__main__':
    init_dispatcher(dp)

    match settings.BOT_MODE:
        case BotMode.WEBHOOK:
            setup(http_app, dp, bot=bot)
            run_app(
                http_app,
                host="0.0.0.0",
                port=settings.WEB_SERVER_PORT,
            )

        case BotMode.POOLING:
            dp.run_polling(bot)

        case _:
            raise ValueError("launch mode must be one of the 'WEBHOOK' or 'POOLING'.")
