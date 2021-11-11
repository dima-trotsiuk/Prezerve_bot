from aiogram import types
from loader import dp
from utils.db_api.select_storage import select_storage_func


@dp.message_handler(text="Вывести склад 🍑")
async def get_storage_func(message: types.Message):
    products = select_storage_func(category=0)
    full_storage = ''
    for product in products:
        full_storage += f'{product[0]}. {product[1]}\nКоличество: <b>{product[3]}</b>шт Цена: <b>{product[5]}</b>грн\n\n'
    await message.answer("<i>Склад:</i>\n"
                         f"{full_storage}")
