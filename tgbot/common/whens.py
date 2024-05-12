from abc import ABC, abstractmethod
from typing import Self, Generic, TypeVar

from aiogram.types import User
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import Whenable

from .mixins import UserIDMixin
from .types import UserIDType

T = TypeVar("T")


class BaseWhen(ABC, Generic[T]):
    def __init__(self, value: T):
        self.value = value
        self._flag = True

    @abstractmethod
    def __call__(self,
                 data: dict,
                 widget: Whenable,
                 manager: DialogManager) -> bool:
        ...

    def __invert__(self) -> Self:
        copy = type(self)(self.value)
        copy._flag = not copy._flag
        return copy


class WhenUserID(BaseWhen[UserIDType], UserIDMixin):
    def __call__(self,
                 _: dict,
                 __: Whenable,
                 manager: DialogManager):
        user: User = manager.middleware_data["event_from_user"]
        user_id = user.id
        if str(user_id) in self.users_id:
            return True
        return False


class WhenKey(BaseWhen[str], ABC):
    pass


class WhenGetterKey(WhenKey):
    def __call__(self,
                 data: dict,
                 _: Whenable,
                 manager: DialogManager):
        result = data.get(self.value)
        return bool(result) == self._flag


class WhenDialogKey(WhenKey):
    def __call__(self,
                 data: dict,
                 _: Whenable,
                 manager: DialogManager):
        result = manager.dialog_data.get(self.value)
        return bool(result) == self._flag
