from aiogram import Router

from .handlers.create import create_sub_dialog
from .handlers.current_list import current_subs_dialog
from .handlers.edit import sub_edit_dialog
from .handlers.main import subs_main_dialog

subs_router = Router(name="subs")
subs_router.include_routers(
    subs_main_dialog,
    create_sub_dialog,
    current_subs_dialog,
    sub_edit_dialog,
)
