from aiogram_dialog.widgets.kbd import SwitchTo
from aiogram_dialog.widgets.text import Const

from .states import SubMenu

ON_MAIN_BUTTON = SwitchTo(
    Const("Назад ◀️"),
    id="main",
    state=SubMenu.main
)
