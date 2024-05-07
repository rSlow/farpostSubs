from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, Protocol, Optional, Callable, Awaitable

from aiogram import types
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import Context


@dataclass
class BaseTypeFactory(Protocol):
    error_text: Optional[str]

    @abstractmethod
    def __call__(self, text: str) -> Any:
        ...


OnFinish = Callable[[types.Message, DialogManager], Awaitable]


class DialogGetter(Protocol):
    @abstractmethod
    async def __call__(self, **kwargs) -> dict:
        ...


class DefaultDialogGetter(DialogGetter):
    async def __call__(self,
                       aiogd_context: Context,
                       **kwargs):
        return aiogd_context.dialog_data
