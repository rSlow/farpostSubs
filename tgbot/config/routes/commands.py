from aiogram import Router

from common.handlers.commands import common_commands_router

commands_router = Router(name="commands")
commands_router.include_routers(
    common_commands_router,
)
