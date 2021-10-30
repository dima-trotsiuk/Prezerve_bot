from aiogram.dispatcher.filters.state import StatesGroup, State


class DeleteOrderAdmin(StatesGroup):
    delete_for_id = State()
