from aiogram.fsm.state import State, StatesGroup


class FSMGetContent(StatesGroup):
    subscribe = State()
    check_link = State()
    user_answer = State()
