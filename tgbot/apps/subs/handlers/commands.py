from aiogram import Router, types
from aiogram.filters import Command
from aiogram_dialog import DialogManager, ShowMode

commands_subs_router = Router(name="commands_subs")


@commands_subs_router.message(Command("help"))
async def command_help(message: types.Message,
                       dialog_manager: DialogManager):
    await message.answer(
        "Для получения нужной ссылки на подписку, необходимо подписаться в приложении FarPost, включить оповещения "
        "по подписке в телеграм и дождаться, когда в телеграм придет сообщение со ссылкой на сохраненный запрос. "
        "Эту ссылку и необходимо вставлять в бота. После получения ссылки уведомления в самом приложении FarPost "
        "можно отключить, они больше не нужны для работы этого бота."
    )
    await dialog_manager.update({}, ShowMode.DELETE_AND_SEND)
