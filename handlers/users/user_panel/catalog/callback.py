from aiogram import types

from keyboards.inline.adminka.globals.select_category import new_product_select_func
from loader import dp


@dp.message_handler(text="Каталог 🏷")
async def get_storage_func(message: types.Message):
    await message.answer(f"Категории:", reply_markup=await new_product_select_func(switch="user"))



