from typing import Any

from aiogram.filters import BaseFilter
from aiogram.types import TelegramObject

from common.types import UserIDType


class UserIDMixin:
    def __init__(self, users_id: UserIDType):
        if not isinstance(users_id, (list, tuple)):
            users_id = (users_id,)
        self.users_id = users_id


class UserIDFilter(BaseFilter, UserIDMixin):

    async def __call__(self,
                       obj: TelegramObject,
                       raw_state: str | None = None) -> bool | dict[str, Any]:
        if str(obj.from_user.id) not in self.users_id:
            return False
        return True
