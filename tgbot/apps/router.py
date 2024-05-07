from aiogram import Router

from apps.subs.router import subs_router

apps_router = Router(name="apps")

apps_router.include_routers(
    subs_router,
)
