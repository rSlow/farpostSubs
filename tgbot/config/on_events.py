from aiogram import Bot, Dispatcher
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from dishka import make_async_container
from dishka.integrations.aiogram import setup_dishka as aiogram_setup_dishka
from loguru import logger

from apps.subs.di.provider import AdsProvider
from apps.subs.mq.broker import ads_broker
from apps.subs.scheduler import AdsScheduler
from common.ORM.database import Session
from common.middlewares import ContextMiddleware, register_middlewares, DbSessionMiddleware
from common.scheduler.functions import init_schedulers
from config import settings
from config.enums import BotMode
from config.logger import init_logging
from config.ui_config import init_ui_commands
from http_server.webhook import init_webhook


async def on_startup(dispatcher: Dispatcher,
                     bot: Bot,
                     **__):
    logger.info("STARTUP")
    init_logging()

    await ads_broker.startup()

    ads_scheduler = AdsScheduler(broker=ads_broker)
    schedulers = {
        "ads_scheduler": ads_scheduler,
    }
    async with Session() as session:
        await init_schedulers(
            schedulers=schedulers,
            session=session
        )

    middlewares = [
        ContextMiddleware(**schedulers),
        DbSessionMiddleware(Session),
        CallbackAnswerMiddleware()
    ]
    register_middlewares(middlewares, dispatcher)

    await init_ui_commands(bot)

    if settings.BOT_MODE == BotMode.WEBHOOK:
        await bot.delete_webhook()
        await init_webhook(bot)


async def on_shutdown(dispatcher: Dispatcher,
                      bot: Bot):
    logger.info("SHUTDOWN")

    await bot.session.close()

    await ads_broker.shutdown()

    if settings.BOT_MODE == BotMode.WEBHOOK:
        await bot.delete_webhook()
