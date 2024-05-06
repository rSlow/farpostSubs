from aiogram import Router

from apps.music.handlers.error import error_music_router
from common.handlers.error import common_error_router

error_router = Router(name="error")
error_router.include_routers(
    error_music_router,
    common_error_router,
)
