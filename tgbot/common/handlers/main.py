from aiogram_dialog import Dialog, Window, LaunchMode
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Const

from apps.subs.states import SubsMainFSM
from ..FSM import CommonFSM

main_menu = Dialog(
    Window(
        Const("Выберите действие:"),
        Start(
            Const("Подписки"),
            state=SubsMainFSM.state,
            id="subs"
        ),
        state=CommonFSM.state,
    ),
    launch_mode=LaunchMode.ROOT
)
