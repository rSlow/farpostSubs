import inspect
from dataclasses import dataclass, field
from functools import wraps
from typing import Optional, no_type_check, Any, Callable, Self

from aiogram import types
from aiogram.fsm.state import StatesGroup, State, StatesGroupMeta
from aiogram.types import UNSET_PARSE_MODE
from aiogram.types.base import UNSET_DISABLE_WEB_PAGE_PREVIEW
from aiogram_dialog import Dialog, Window, LaunchMode, DialogManager, ShowMode
from aiogram_dialog.api.internal.widgets import MarkupFactory
from aiogram_dialog.dialog import OnResultEvent, OnDialogEvent
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.input.text import OnSuccess, OnError, TextInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import Keyboard, Cancel, Back, Next, Row
from aiogram_dialog.widgets.kbd.button import OnClick
from aiogram_dialog.widgets.markup.inline_keyboard import InlineKeyboardFactory
from aiogram_dialog.widgets.text import Const, Text, Format
from aiogram_dialog.widgets.utils import GetterVariant

from common.buttons import MAIN_MENU_BUTTON
from common.dialogs.factory.protocols import BaseTypeFactory, OnFinish, DefaultDialogGetter


def _get_cancel_button(text: Text = Const("Назад ◀"),
                       _id: str = "__cancel__",
                       result: Any | None = None,
                       on_click: Optional[OnClick] = None,
                       when: WhenCondition = None):
    return Cancel(
        text=text, id=_id,
        result=result, on_click=on_click,
        when=when
    )


def _get_back_button(text: Text = Const("Назад ◀"),
                     _id: str = "__back__",
                     on_click: Optional[OnClick] = None,
                     when: WhenCondition = None):
    return Back(
        text=text, id=_id,
        on_click=on_click, when=when
    )


def _get_next_button(text: Text = Const("Вперед ▶"),
                     _id: str = "__next__",
                     on_click: Optional[OnClick] = None,
                     when: WhenCondition = None):
    return Next(
        text=text, id=_id,
        on_click=on_click, when=when
    )


class FormState(State):
    def __init__(self,
                 *texts: Text,
                 keyboard: Optional[Keyboard] = None,
                 type_factory: Optional[type[BaseTypeFactory]] = str,
                 on_success: Optional[OnSuccess] = None,
                 on_error: Optional[OnError] = None,
                 _filter: Optional[Callable[..., Any]] = None,
                 show_current_value: Optional[bool] = True,
                 current_value_text: Optional[Text] = None,
                 getter: GetterVariant = None,
                 state: Optional[str] = None,
                 group_name: Optional[str] = None):
        super().__init__(state, group_name)

        self.texts = texts
        self.keyboard = keyboard
        self.type_factory = type_factory
        self._on_success = on_success
        self._on_error = on_error
        self.filter = _filter
        self.show_current_value = show_current_value
        self.current_value_text = current_value_text
        self.getter = getter

    @property
    def on_success(self):
        if self._on_success is None:
            return self._default_on_success
        return self._on_success

    @property
    def on_error(self):
        if self._on_error is None:
            return self._default_on_error
        return self._on_success

    @property
    def state_name(self):
        return self.state.split(":")[-1]

    @staticmethod
    async def _default_on_success(_: types.Message,
                                  text_input: ManagedTextInput,
                                  manager: DialogManager,
                                  text: str):
        widget_id = text_input.widget.widget_id
        manager.dialog_data.update({widget_id: text})
        try:
            await manager.next()
        except IndexError:
            pass

    async def _default_on_error(self,
                                message: types.Message,
                                _: ManagedTextInput,
                                manager: DialogManager,
                                __: ValueError):
        manager.show_mode = ShowMode.DELETE_AND_SEND
        type_factory = self.type_factory()
        if type_factory.error_text is not None:
            await message.answer(type_factory.error_text)

    def copy(self):
        cls: type[Self] = type(self)
        return cls(
            *self.texts,
            state=self._state,
            group_name=self._group_name,
            keyboard=self.keyboard,
            type_factory=self.type_factory,
            on_success=self._on_success,
            on_error=self._on_error,
            _filter=self.filter,
            show_current_value=self.show_current_value,
            current_value_text=self.current_value_text,
            getter=self.getter
        )


class FormStatesGroupMeta(StatesGroupMeta):
    __states__: tuple[FormState, ...]

    @no_type_check
    def __new__(mcs, name, bases, namespace, **kwargs):
        cls = super(FormStatesGroupMeta, mcs).__new__(mcs, name, bases, namespace)

        states = []
        childs = []

        base: mcs = bases[0]
        for base_state in base:
            if isinstance(base_state, FormState):
                state_name = base_state.state_name
                state_copy = base_state.copy()
                state_copy.set_parent(cls)
                namespace[state_name] = state_copy

        for name, arg in namespace.items():
            if isinstance(arg, FormState):
                states.append(arg)
            elif inspect.isclass(arg) and issubclass(arg, FormStatesGroup):
                childs.append(arg)
                arg.__parent__ = cls

        cls.__parent__ = None
        cls.__childs__ = tuple(childs)
        cls.__states__ = tuple(states)
        cls.__state_names__ = tuple(state.state for state in states)

        return cls


class FormStatesGroup(StatesGroup, metaclass=FormStatesGroupMeta):
    @classmethod
    def first(cls) -> FormState:
        return cls.__states__[0]

    @classmethod
    def get_states(cls):
        return cls.__states__

    def __len__(self):
        return len(self.get_states())


DEFAULT_MARKUP_FACTORY = InlineKeyboardFactory()


class WindowTemplate:
    def __init__(self,
                 markup_factory: MarkupFactory = DEFAULT_MARKUP_FACTORY,
                 parse_mode: Optional[str] = UNSET_PARSE_MODE,
                 disable_web_page_preview: Optional[bool] = UNSET_DISABLE_WEB_PAGE_PREVIEW,
                 preview_add_transitions: Optional[list[Keyboard]] = None,
                 preview_data: GetterVariant = None,
                 add_main_menu_button: bool = False):
        self.markup_factory = markup_factory
        self.parse_mode = parse_mode
        self.disable_web_page_preview = disable_web_page_preview
        self.preview_add_transitions = preview_add_transitions
        self.preview_data = preview_data
        self.add_main_menu_button = add_main_menu_button


@dataclass
class TextInputDialogFactory:
    states_group: type[FormStatesGroup]
    on_finish: OnFinish
    template: WindowTemplate = field(default_factory=WindowTemplate)

    def _on_click_last_state(self, on_success: OnSuccess) -> OnSuccess:
        @wraps(self.on_finish)
        async def _on_success(message: types.Message,
                              text_input: ManagedTextInput,
                              manager: DialogManager,
                              text: str):
            await on_success(message, text_input, manager, text)
            await self.on_finish(message, manager)

        return _on_success

    def create_dialog(self,
                      on_start: Optional[OnDialogEvent] = None,
                      on_close: Optional[OnDialogEvent] = None,
                      on_process_result: Optional[OnResultEvent] = None,
                      launch_mode: LaunchMode = LaunchMode.STANDARD,
                      getter: GetterVariant = DefaultDialogGetter(),
                      preview_data: GetterVariant = None,
                      name: Optional[str] = None):
        windows = []
        for i, state in enumerate(self.states_group.get_states(), 1):
            state_name = state.state_name
            widgets = [*state.texts]

            if i != len(self.states_group.get_states()):
                _on_success = state.on_success
            else:
                _on_success = self._on_click_last_state(state.on_success)
            widgets.append(
                TextInput(
                    id=state_name,
                    type_factory=state.type_factory(),
                    on_success=_on_success,
                    on_error=state.on_error,
                    filter=state.filter
                )
            )

            if state.show_current_value:
                if state.current_value_text is None:
                    state.current_value_text = Format(
                        "\nТекущее значение - <i>{" + state_name + "}</i>",
                        when=state_name
                    )
                widgets.append(state.current_value_text)

            if state.keyboard is not None:
                widgets.append(state.keyboard)

            if i == 1:
                widgets.append(Row(
                    _get_cancel_button(),
                    _get_next_button(when=state.state_name)
                ))
            elif i == len(self.states_group.get_states()):
                widgets.append(_get_back_button())
            else:
                widgets.append(
                    Row(
                        _get_back_button(),
                        _get_next_button(when=state.state_name)
                    )
                )

            if self.template.add_main_menu_button:
                widgets.append(MAIN_MENU_BUTTON)

            window = Window(
                *widgets,
                getter=state.getter,
                markup_factory=self.template.markup_factory,
                parse_mode=self.template.parse_mode,
                disable_web_page_preview=self.template.disable_web_page_preview,
                preview_add_transitions=self.template.preview_add_transitions,
                preview_data=self.template.preview_data,
                state=state,
            )
            windows.append(window)

        return Dialog(
            *windows,
            on_start=on_start,
            on_close=on_close,
            on_process_result=on_process_result,
            launch_mode=launch_mode,
            getter=getter,
            preview_data=preview_data,
            name=name,
        )
