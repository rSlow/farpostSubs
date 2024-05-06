from aiogram import Router

from apps.birthdays.handlers.command import birthdays_command_router
from common.handlers.commands import common_commands_router

commands_router = Router(name="commands")
commands_router.include_routers(
    birthdays_command_router,
    common_commands_router,
)
