from aiogram.dispatcher.filters.state import StatesGroup, State


class AddOrderAdmin(StatesGroup):
    add_product = State()
    new_value = State()
    set_ttn = State()
