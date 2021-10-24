from aiogram.dispatcher.filters.state import StatesGroup, State


class NewValueQuantity(StatesGroup):
    new_value = State()


class NewValueOther(StatesGroup):
    new_value_other = State()
    info = State()
