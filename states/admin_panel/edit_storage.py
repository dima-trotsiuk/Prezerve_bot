from aiogram.dispatcher.filters.state import StatesGroup, State


class NewProduct(StatesGroup):
    title = State()
    photo = State()
    content = State()
    quantity = State()
    price = State()


