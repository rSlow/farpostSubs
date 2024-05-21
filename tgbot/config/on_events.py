from aiogram import Bot, Dispatcher
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from dishka import make_async_container
from dishka.integrations.aiogram import setup_dishka as aiogram_setup_dishka
from dishka.integrations.taskiq import setup_dishka as taskiq_setup_dishka
from loguru import logger
from taskiq_aio_pika import AioPikaBroker

from apps.subs.di.provider import AdsProvider
from apps.subs.scheduler import AdsScheduler
from common.ORM.database import Session
from common.di.sql_provider import SQLProvider
from common.middlewares import DbSessionMiddleware, ContextMiddleware, register_middlewares
from common.scheduler import init_schedulers
from config import settings
from config.enums import BotMode
from config.logger import init_logging
from config.ui_config import set_ui_commands
from http_server.webhook import init_webhook


async def on_startup(dispatcher: Dispatcher,
                     bot: Bot,
                     **__):
    logger.info("STARTUP")
    init_logging()

    container = make_async_container(
        AdsProvider(), SQLProvider(),
        context={Bot: bot}
    )
    async with container() as container_request:
        ads_broker = await container_request.get(AioPikaBroker)
    taskiq_setup_dishka(container, ads_broker)
    aiogram_setup_dishka(container, dispatcher)

    schedulers = {
        "ads_scheduler": AdsScheduler(broker=ads_broker),
    }
    await init_schedulers([*schedulers.values()])

    middlewares = [
        ContextMiddleware(
            **schedulers,
        ),
        DbSessionMiddleware(session_pool=Session),
        CallbackAnswerMiddleware()
    ]
    register_middlewares(middlewares, dispatcher)

    await set_ui_commands(bot)

    if settings.BOT_MODE == BotMode.WEBHOOK:
        await bot.delete_webhook()
        await init_webhook(bot)


async def on_shutdown(dispatcher: Dispatcher,
                      bot: Bot):
    logger.info("SHUTDOWN")
    await bot.session.close()

    if settings.BOT_MODE == BotMode.WEBHOOK:
        await bot.delete_webhook()
