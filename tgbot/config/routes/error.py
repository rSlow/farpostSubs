from aiogram import Router

from common.handlers.error import common_error_router

error_router = Router(name="error")
error_router.include_routers(
    common_error_router,
)
