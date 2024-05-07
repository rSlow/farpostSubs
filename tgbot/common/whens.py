from typing import Self

from aiogram.types import User
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import Whenable

from .filters import UserIDMixin


class WhenUserID(UserIDMixin):
    def __call__(self,
                 _: dict,
                 __: Whenable,
                 manager: DialogManager):
        user: User = manager.middleware_data["event_from_user"]
        user_id = user.id
        if str(user_id) in self.users_id:
            return True
        return False


class WhenAble:
    def __init__(self,
                 key: str,
                 flag: bool = True):
        self.key = key
        self.flag = flag

    def __call__(self,
                 data: dict,
                 _: Whenable,
                 __: DialogManager):
        result = data.get(self.key)
        return bool(result) == self.flag

    def __invert__(self) -> Self:
        return type(self)(self.key, not self.flag)
