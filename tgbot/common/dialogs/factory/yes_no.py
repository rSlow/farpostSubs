from aiogram import types
from aiogram.fsm.state import State
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Row, Cancel, SwitchTo
from aiogram_dialog.widgets.kbd.button import OnClick, Button
from aiogram_dialog.widgets.text import Text, Const
from aiogram_dialog.widgets.utils import GetterVariant


def done_dialog_wrapper(on_click: OnClick):
    async def inner(callback: types.CallbackQuery,
                    button: Button,
                    manager: DialogManager):
        await on_click(callback, button, manager)
        await manager.done()

    return inner


def yes_no_dialog(*texts: Text,
                  state: State,
                  on_click: OnClick,
                  getter: GetterVariant = None):
    return Dialog(
        Window(
            *texts,
            Row(
                Button(
                    Const("Да"),
                    on_click=done_dialog_wrapper(on_click),
                    id="yes"
                ),
                Cancel(Const("Нет"))
            ),
            state=state,
            getter=getter
        )
    )


def yes_no_window(*texts: Text,
                  state: State,
                  back_state: State,
                  on_click: OnClick,
                  getter: GetterVariant = None):
    return Window(
        *texts,
        Row(
            Button(
                Const("Да"),
                on_click=on_click,
                id="yes"
            ),
            SwitchTo(
                text=Const("Нет"),
                id="no",
                state=back_state
            )
        ),
        state=state,
        getter=getter
    )
