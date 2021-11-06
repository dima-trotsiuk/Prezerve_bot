from aiogram import types

from filters import IsAdmin
from keyboards.default import admin_menu
from loader import dp
from aiogram.dispatcher.filters import Command


@dp.message_handler(Command("menu"), IsAdmin())
async def show_menu(message: types.Message):
    await message.answer("Что пожелает господин?", reply_markup=admin_menu)
