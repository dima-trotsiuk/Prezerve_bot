from aiogram.dispatcher.filters.state import StatesGroup, State


class EditOrderAdmin(StatesGroup):
    edit_for_id = State()
    command = State()
