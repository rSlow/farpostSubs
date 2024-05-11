from aiogram import Router

from apps.subs.handlers.commands import commands_subs_router
from common.handlers.commands import common_commands_router

commands_router = Router(name="commands")
commands_router.include_routers(
    common_commands_router,
    commands_subs_router,
)
