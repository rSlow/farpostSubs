from aiogram_dialog.widgets.kbd import Start, Cancel, Back, Next
from aiogram_dialog.widgets.text import Const

from common.FSM import CommonFSM

MAIN_MENU_BUTTON = Start(
    text=Const("Главное меню ☰"),
    id="__main__",
    state=CommonFSM.state,
)

CANCEL_BUTTON = Cancel(
    text=Const("Назад ◀")
)

BACK_BUTTON = Back(
    text=Const("Назад ◀")
)
NEXT_BUTTON = Next(
    text=Const("Вперед ◀")
)
