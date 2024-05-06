from aiogram_dialog import Dialog, Window, LaunchMode
from aiogram_dialog.widgets.text import Format

from ..FSM import CommonFSM

main_menu = Dialog(
    Window(
        Format("Выберите действие:"),
        state=CommonFSM.state,
    ),
    launch_mode=LaunchMode.ROOT
)
