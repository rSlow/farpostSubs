from aiogram import Router

from apps.subs.handlers.errors import subs_error_router
from common.handlers.error import common_error_router

error_router = Router(name="error")
error_router.include_routers(
    subs_error_router,
    common_error_router,
)
