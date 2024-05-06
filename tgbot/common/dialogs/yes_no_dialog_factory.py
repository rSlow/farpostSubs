from aiogram.fsm.state import State
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Row, Cancel
from aiogram_dialog.widgets.kbd.button import OnClick, Button
from aiogram_dialog.widgets.text import Text, Const


def yes_no_dialog_factory(*texts: Text,
                          state: State,
                          on_click: OnClick):
    return Dialog(
        Window(
            *texts,
            Row(
                Button(
                    Const("Да"),
                    on_click=on_click,
                    id="yes"
                ),
                Cancel(Const("Нет"))
            ),
            state=state
        )
    )
