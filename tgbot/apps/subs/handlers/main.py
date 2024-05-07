from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Const

from common.buttons import CANCEL_BUTTON
from ..states import SubsMainFSM, CreateSub, CurrentSubsFSM

subs_main_dialog = Dialog(
    Window(
        Const("Выберите действие"),
        Start(
            Const("Текущие подписки"),
            state=CurrentSubsFSM.state,
            id="current"
        ),
        Start(
            Const("Добавить подписку"),
            state=CreateSub.url,
            id="current"
        ),
        CANCEL_BUTTON,
        state=SubsMainFSM.state
    )
)
