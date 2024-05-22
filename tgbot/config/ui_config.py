from aiogram import Bot
from aiogram.types import BotCommandScopeAllPrivateChats, BotCommand


async def init_ui_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="На главную"),
        BotCommand(command="menu", description="Показать меню"),
        BotCommand(command="help", description="Помощь"),
    ]
    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeAllPrivateChats()
    )
