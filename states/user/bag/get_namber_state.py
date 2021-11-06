from aiogram.dispatcher.filters.state import StatesGroup, State


class GetNumber(StatesGroup):
    number = State()
