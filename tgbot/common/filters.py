import re
from typing import Any, Optional

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


def regexp_factory(pattern: str | re.Pattern[str],
                   error_message: Optional[str] = None):
    def _factory(value: str):
        res = re.match(pattern, value)
        if res is None:
            raise ValueError(error_message.format(value=value)
                             if error_message
                             else f"{value} is not matched with pattern {pattern}")
        return res.group()

    return _factory
