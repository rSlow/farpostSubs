import asyncio
from typing import Optional

from aiogram import Router, types
from aiogram.filters import ExceptionTypeFilter
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.api.exceptions import NoContextError, UnknownIntent
from loguru import logger

from common.FSM import CommonFSM
from common.utils.functions import get_message

common_error_router = Router(name="common_errors")


@common_error_router.error(ExceptionTypeFilter(NoContextError, UnknownIntent))
async def context_error(event: types.ErrorEvent,
                        dialog_manager: DialogManager):
    response_message = await other_errors(
        event=event,
        dialog_manager=dialog_manager,
        message_text="Ошибка кэша бота. Возврат в главное меню..."
    )
    await asyncio.sleep(2)
    await response_message.delete()


@common_error_router.error()
async def other_errors(event: types.ErrorEvent,
                       dialog_manager: DialogManager,
                       message_text: Optional[str] = None):
    logger.exception(event.exception)
    message = get_message(event)
    _default_text = (f"Извините, во время работы бота произошла ошибка. Мы вынуждены вернуть вас на главный экран. "
                     f"Попробуйте воспользоваться функцией еще раз.")
    response_message = await message.answer(message_text or _default_text)
    await dialog_manager.start(
        state=CommonFSM.state,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.SEND
    )
    return response_message
