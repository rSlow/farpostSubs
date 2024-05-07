from aiogram import Router

from .handlers.create import create_sub_dialog
from .handlers.current import current_subs_dialog
from .handlers.main import subs_main_dialog

subs_router = Router(name="subs")
subs_router.include_routers(
    subs_main_dialog,
    current_subs_dialog,
    create_sub_dialog,
)
