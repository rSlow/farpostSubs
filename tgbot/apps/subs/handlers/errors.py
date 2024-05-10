from aiogram import Router, types
from aiogram.filters import ExceptionTypeFilter
from aiogram_dialog import DialogManager, ShowMode

from common.utils.functions import get_message
from ..exceptions import AlreadyExistsError

subs_error_router = Router(name="subs_error")


@subs_error_router.error(ExceptionTypeFilter(AlreadyExistsError))
async def equal_subs_exist(event: types.ErrorEvent,
                           dialog_manager: DialogManager):
    message = get_message(event)
    await message.answer(event.exception.args[0])
    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
    await dialog_manager.done()
