from aiogram import types
from aiogram.types import CallbackQuery

from keyboards.inline.adminka.edit_storage_buttons.edit_product import edit_product_for_id
from keyboards.inline.adminka.globals.callback_datas import select_products_callback
from keyboards.inline.adminka.globals.show_storage import show_storage_func
from loader import dp

from keyboards.inline.adminka.globals.select_category import new_product_select_func


@dp.message_handler(text="🤡 Редактировать склад 🤡")
async def get_storage_func(message: types.Message):
    await message.answer("Вы хотите 🤡 Редактировать склад 🤡",
                         reply_markup=await show_storage_func(switch="edit_storage"))


@dp.callback_query_handler(select_products_callback.filter(type_command="edit_storage_admin"))
async def order_managment_admin_call(call: CallbackQuery, callback_data: dict):
    await call.answer()
    if callback_data.get("id") == "new_product":
        await call.message.answer("Категория?", reply_markup=await new_product_select_func(switch="new_product"))
    else:
        id_product = callback_data.get("id")
        await edit_product_for_id(id_product, call.message)
