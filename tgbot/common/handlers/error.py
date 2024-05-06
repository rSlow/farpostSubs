from aiogram import Router, types
from aiogram_dialog import DialogManager, StartMode, ShowMode

from common.FSM import CommonFSM
from loguru import logger

common_error_router = Router(name="common_errors")


@common_error_router.error()
async def key_error_pass(event: types.ErrorEvent,
                         dialog_manager: DialogManager):
    message = event.update.message if event.update.message is not None else event.update.callback_query.message
    await message.answer(
        f"Извините, во время работы бота произошла ошибка. "
        f"Мы вынуждены вернуть вас на главный экран. "
        f"Попробуйте воспользоваться функцией еще раз."
    )
    logger.exception(event.exception)
    await dialog_manager.start(
        state=CommonFSM.state,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.SEND
    )
