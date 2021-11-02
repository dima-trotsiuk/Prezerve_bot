from aiogram import types
from loader import dp


@dp.message_handler(text="Каталог 🏷")
async def get_storage_func(message: types.Message):
    await message.answer(f"Данный раздел в разработке")