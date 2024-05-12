from aiogram import Router, types
from aiogram.filters import Command
from aiogram_dialog import DialogManager, ShowMode

commands_subs_router = Router(name="commands_subs")


@commands_subs_router.message(Command("help"))
async def command_help(message: types.Message,
                       dialog_manager: DialogManager):
    await message.answer(
        "Бот отслеживает новые предложения для выбранного запроса на сайте FarPost. Для отслеживания новых "
        "предложений зайдите на сайт или в приложение FarPost, сформируйте запрос по нужным Вам критериям, и "
        "скопируйте ссылку на получившийся запрос. Создайте подписку в боте, отправив данную ссылку. Также можно "
        "настроить периодичность проверки запроса."
    )
    await dialog_manager.update({}, ShowMode.DELETE_AND_SEND)
