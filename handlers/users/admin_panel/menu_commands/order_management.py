from aiogram import types
from aiogram.types import CallbackQuery

from keyboards.inline.order_management_buttons.callback_datas import order_management_callback
from keyboards.inline.order_management_buttons.order_managment_buttons import order_management
from loader import dp


@dp.message_handler(text="😎 Управление заказами 😎")
async def get_storage_func(message: types.Message):
    await message.answer("😎 Управление заказами 😎", reply_markup=order_management)


@dp.callback_query_handler(order_management_callback.filter(type_command="order_managment_admin"))
async def order_managment_admin_call(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)

    command = callback_data.get("command")
    await call.message.answer(f"{command}")
