from aiogram import Bot, Dispatcher
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from loguru import logger

from apps.subs.scheduler import SubsScheduler
from common.ORM.database import Session
from common.middlewares import DbSessionMiddleware, ContextMiddleware, register_middlewares
from common.mq.manager import RabbitConnectionManager
from common.mq.schemas import MQConnectionConfig, MQExchangeConfig, MQQueueConfig
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

    rabbit_connection = RabbitConnectionManager(
        connection_config=MQConnectionConfig(url=settings.RABBITMQ_URL),
        exchange_config=MQExchangeConfig(
            name="ads",
            publisher_confirms=False
        ),
        queue_config=MQQueueConfig(name="ads")
    )
    await rabbit_connection.create()

    schedulers = {
        "subs_scheduler": SubsScheduler(
            bot=bot,
            dispatcher=dispatcher,
            rabbit=rabbit_connection
        ),
    }
    await init_schedulers([*schedulers.values()])

    middlewares = [
        ContextMiddleware(
            rabbit_connection=rabbit_connection,
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
