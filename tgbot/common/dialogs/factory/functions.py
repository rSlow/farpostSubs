from abc import abstractmethod
from typing import TypeVar, Optional, Protocol, Any, Callable

from aiogram import types
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import ManagedTextInput

T = TypeVar("T")


class AfterHandler(Protocol):
    @abstractmethod
    async def __call__(self,
                       message: types.Message,
                       manager: DialogManager,
                       data: T):
        ...


PreSaver = Callable[[T], Any]


class OnValidInput:
    def __init__(self,
                 key_name: Optional[str] = None,
                 delete_input: bool = True,
                 handle_next: bool = True,
                 mode: ShowMode = ShowMode.EDIT,
                 after_handler: Optional[AfterHandler] = None,
                 pre_saver: Optional[PreSaver] = None):
        self.key_name = key_name
        self.delete_input = delete_input
        self.handle_next = handle_next
        self.mode = mode
        self.after_handler = after_handler
        self.pre_saver = pre_saver

    async def __call__(self,
                       message: types.Message,
                       text_input: ManagedTextInput[T],
                       dialog_manager: DialogManager,
                       data: T):
        dialog_manager.show_mode = self.mode
        if self.key_name is None:
            self.key_name = text_input.widget.widget_id
        if self.pre_saver is not None:
            data = self.pre_saver(data)
        dialog_manager.dialog_data[self.key_name] = data

        if self.delete_input:
            await message.delete()
        if self.after_handler is not None:
            await self.after_handler(message, dialog_manager, data)
        if self.handle_next:
            await dialog_manager.next()


class OnInvalidInput:
    def __init__(self,
                 error_message: str,
                 mode: ShowMode = ShowMode.DELETE_AND_SEND,
                 delete_input: bool = False):
        self.error_message = error_message
        self.mode = mode
        self.delete_input = delete_input

    async def __call__(self,
                       message: types.Message,
                       text_input: ManagedTextInput[T],
                       dialog_manager: DialogManager,
                       error: ValueError):
        dialog_manager.show_mode = self.mode
        message_text = self.error_message.format(
            message=message,
            error=error,
            data=text_input.get_value()
        )
        await message.answer(message_text)
        if self.delete_input:
            await message.delete()
