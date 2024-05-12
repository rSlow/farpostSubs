from __future__ import annotations

from abc import abstractmethod
from typing import Protocol, Optional

from aiogram_dialog import DialogManager, ChatEvent
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.kbd.checkbox import BaseCheckbox
from aiogram_dialog.widgets.text import Text


class OnStateChanged(Protocol):
    @abstractmethod
    async def __call__(self,
                       event: ChatEvent,
                       checkbox: DataCheckbox,
                       manager: DialogManager):
        ...


class DataCheckbox(BaseCheckbox):
    def __init__(self,
                 checked_text: Text,
                 unchecked_text: Text,
                 id: str,
                 data_getter: str,
                 on_state_changed: Optional[OnStateChanged] = None,
                 when: WhenCondition = None):
        super().__init__(
            checked_text=checked_text, unchecked_text=unchecked_text,
            id=id, when=when, on_state_changed=on_state_changed
        )
        self.data_getter = data_getter

    def is_checked(self, manager: DialogManager) -> bool:
        return bool(manager.dialog_data.get(self.data_getter, False))

    async def set_checked(self,
                          event: ChatEvent,
                          checked: bool,
                          manager: DialogManager) -> None:
        manager.dialog_data[self.data_getter] = checked
        await self.on_state_changed.process_event(
            event, self.managed(manager), manager,
        )
