from .types import UserIDType


class UserIDMixin:
    def __init__(self, users_id: UserIDType):
        if not isinstance(users_id, (list, tuple)):
            users_id = (users_id,)
        self.users_id = users_id
