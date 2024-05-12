from aiogram import Dispatcher
from aiogram.fsm.storage.memory import SimpleEventIsolation
from aiogram_dialog import setup_dialogs
from loguru import logger

from apps.router import apps_router
from common.handlers.main import main_menu
from . import settings
from .on_events import on_startup, on_shutdown
from .routes.commands import commands_router
from .routes.error import error_router
from .routes.events import events_router
from .routes.test import test_router
from .storage import redis_storage

dp = Dispatcher(
    storage=redis_storage,
    events_isolation=SimpleEventIsolation()
)


def init_dispatcher(dispatcher: Dispatcher):
    dispatcher.startup.register(on_startup)
    dispatcher.shutdown.register(on_shutdown)

    setup_dialogs(dispatcher)

    dispatcher.include_routers(
        events_router,
        commands_router,
        error_router,
        main_menu,
        apps_router,
    )

    if settings.DEBUG:
        logger.info("SET DEBUG MODE")

        dispatcher.include_routers(test_router)
