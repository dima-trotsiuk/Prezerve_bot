from aiogram import types
from loader import dp
from utils.db_api.select_storage import select_storage_func


@dp.message_handler(text="Вывести склад 🍑")
async def get_storage_func(message: types.Message):
    products = select_storage_func(category=0)
    full_storage = ''
    for product in products:
        full_storage += f'{product[0]:02}. "{product[1]}" - {product[3]}шт ({product[5]}грн)\n'
    await message.answer("Склад:\n"
                         f"{full_storage}")
