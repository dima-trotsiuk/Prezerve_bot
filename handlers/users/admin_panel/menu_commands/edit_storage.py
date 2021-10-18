from aiogram import types
from aiogram.types import CallbackQuery
from loader import dp
from keyboards.inline.callback_datas import edit_storage_callback
from keyboards.inline.edit_storage_buttons import edit_storage


@dp.message_handler(text="🤡 Редактировать склад 🤡")
async def get_storage_func(message: types.Message):
    await message.answer("Вы хотите 🤡 Редактировать склад 🤡", reply_markup=edit_storage)


@dp.callback_query_handler(edit_storage_callback.filter(type_command="edit_storage_admin"))
async def order_managment_admin_call(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    if callback_data.get("id") == "new_product":
        await call.message.answer(f"+")
    else:
        id = callback_data.get("id")
        await call.message.answer(f"{id}")
