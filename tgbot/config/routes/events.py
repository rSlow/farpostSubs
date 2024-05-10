from aiogram import Router

from common.handlers.events import common_events_router

events_router = Router(name="events")
events_router.include_routers(
    common_events_router,
)
