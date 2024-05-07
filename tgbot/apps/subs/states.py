from aiogram.fsm.state import StatesGroup, State

from common.FSM import FSMSingleFactory

SubsMainFSM = FSMSingleFactory("SubsMainFSM", "main")
CurrentSubsFSM = FSMSingleFactory("CurrentSubsFSM", "main")


class CreateSub(StatesGroup):
    url = State()
    frequency = State()
