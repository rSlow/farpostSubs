from aiogram import types, Router
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode

from ..FSM import CommonFSM

common_commands_router = Router(name="common_commands")


@common_commands_router.message(Command("start", "cancel"))
async def command_start(_: types.Message,
                        dialog_manager: DialogManager):
    await dialog_manager.start(
        state=CommonFSM.state,
        mode=StartMode.RESET_STACK
    )


@common_commands_router.message(Command("menu"))
async def command_menu(_: types.Message,
                       dialog_manager: DialogManager):
    await dialog_manager.update({})
