from aiogram import types
from loader import dp


@dp.message_handler(text="Статистика 🍌")
async def get_storage_func(message: types.Message):

    await message.answer("Нету статистики ((")
