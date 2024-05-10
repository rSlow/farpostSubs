from aiogram.fsm.state import StatesGroup, State

from common.FSM import FSMSingleFactory

SubsMainFSM = FSMSingleFactory("SubsMainFSM", "main")
CurrentSubsFSM = FSMSingleFactory("CurrentSubsFSM", "main")


class SubMenu(StatesGroup):
    main = State()
    name = State()
    frequency = State()
    delete = State()


class CreateSub(StatesGroup):
    url = State()
    frequency = State()
    name = State()
