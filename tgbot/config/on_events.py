from aiogram import Bot, Dispatcher
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from loguru import logger

from apps.subs.mq.manager import init_subs_mq
from apps.subs.scheduler import SubsScheduler
from common.ORM.database import Session
from common.middlewares import DbSessionMiddleware, ContextMiddleware, register_middlewares
from common.scheduler.functions import init_schedulers
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

    subs_mq = await init_subs_mq()

    schedulers = {
        "subs_scheduler": SubsScheduler(
            bot=bot,
            dispatcher=dispatcher,
            rabbit=subs_mq
        ),
    }
    await init_schedulers([*schedulers.values()])

    middlewares = [
        ContextMiddleware(**schedulers),
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
