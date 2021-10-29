from aiogram.dispatcher.filters.state import StatesGroup, State


class AddOrderAdmin(StatesGroup):
    new_value = State()
    set_ttn = State()
