from aiogram import types

from keyboards.inline.user.contacts.link_to_instagram import link_to_instagram_button
from loader import dp


@dp.message_handler(text="Контакты ✉")
async def get_storage_func(message: types.Message):
    await message.answer("Вы всегда можете связатся с нами☺", reply_markup=link_to_instagram_button)