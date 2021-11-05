from aiogram.dispatcher.filters.state import StatesGroup, State


class EditQuantity(StatesGroup):
    quantity = State()
