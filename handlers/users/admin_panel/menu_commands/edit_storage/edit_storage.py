from aiogram import types
from aiogram.types import CallbackQuery

from keyboards.inline.edit_storage_buttons.edit_product import edit_product_for_id
from loader import dp
from keyboards.inline.edit_storage_buttons.callback_datas import edit_storage_callback
from keyboards.inline.edit_storage_buttons.show_storage import show_storage_func
from keyboards.inline.edit_storage_buttons.new_product_select_category import new_product_select_func


@dp.message_handler(text="🤡 Редактировать склад 🤡")
async def get_storage_func(message: types.Message):
    await message.answer("Вы хотите 🤡 Редактировать склад 🤡", reply_markup=await show_storage_func())


@dp.callback_query_handler(edit_storage_callback.filter(type_command="edit_storage_admin"))
async def order_managment_admin_call(call: CallbackQuery, callback_data: dict):
    await call.answer()
    if callback_data.get("id") == "new_product":
        await call.message.answer(f"Выберите категорию:", reply_markup=await new_product_select_func())
    else:
        id_product = callback_data.get("id")
        await edit_product_for_id(id_product, call.message)


