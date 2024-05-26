from types import TracebackType
from typing import Optional, Any

from faststream import BaseMiddleware


class RetryMiddleware(BaseMiddleware):
    def __init__(self,
                 retry: int,
                 msg: Optional[Any] = None):
        self.retry = retry
        super().__init__(msg=msg)

    async def on_receive(self):
        print(f"Received: {self.msg}")
        return await super().on_receive()

    async def after_processed(self,
                              exc_type: Optional[type[BaseException]] = None,
                              exc_val: Optional[BaseException] = None,
                              exc_tb: Optional["TracebackType"] = None, ) -> Optional[bool]:
        return await super().after_processed(exc_type, exc_val, exc_tb)
