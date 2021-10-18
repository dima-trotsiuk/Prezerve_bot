from aiogram import types
from loader import dp


@dp.message_handler(text="🗿 Поиск по ТТН 🗿")
async def get_storage_func(message: types.Message):

    await message.answer("Вы хотите 🗿 Поиск по ТТН 🗿")
