from functools import wraps
from typing import TypeVar

from aiogram import types
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import ManagedTextInput

T = TypeVar("T")


def on_valid_input(key_name: str,
                   handle_next: bool = True):
    @wraps(on_valid_input)
    async def _inner(_: types.Message,
                     __: ManagedTextInput[T],
                     dialog_manager: DialogManager,
                     data: T):
        dialog_manager.dialog_data[key_name] = data.query_params()
        if handle_next:
            await dialog_manager.next()

    return _inner


def on_invalid_input(error_message: str,
                     mode: ShowMode = ShowMode.DELETE_AND_SEND):
    @wraps(on_invalid_input)
    async def _inner(message: types.Message,
                     __: ManagedTextInput[T],
                     dialog_manager: DialogManager,
                     error: ValueError):
        message_text = error_message.format({
            "message": message,
            "error": error,
        })
        await message.answer(message_text)
        dialog_manager.show_mode = mode

    return _inner
