from aiogram import types, Router
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode, ShowMode

from ..FSM import CommonFSM

common_commands_router = Router(name="common_commands")


@common_commands_router.message(Command("start", "cancel"))
async def command_start_process(message: types.Message,
                                dialog_manager: DialogManager):
    preparing_message = await message.answer(
        text="Подготовка...",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await preparing_message.delete()
    await dialog_manager.start(
        state=CommonFSM.state,
        mode=StartMode.RESET_STACK
    )


@common_commands_router.message(Command("help"))
async def command_help(message: types.Message,
                       dialog_manager: DialogManager):
    await message.answer(
        "Для получения нужной ссылки на подписку, необходимо подписаться в приложении FarPost, включить оповещения "
        "по подписке в телеграм и дождаться, когда в телеграм придет сообщение со ссылкой на сохраненный запрос. "
        "Эту ссылку и необходимо вставлять в бота. После получения ссылки уведомления в самом приложении FarPost "
        "можно отключить, они больше не нужны для работы этого бота."
    )
    await dialog_manager.update({}, ShowMode.DELETE_AND_SEND)
