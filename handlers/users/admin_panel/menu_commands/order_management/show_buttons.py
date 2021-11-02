from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from handlers.users.admin_panel.menu_commands.order_management.send_orders import send_orders_func
from handlers.users.admin_panel.menu_commands.order_management.show_orders import show_orders_func
from keyboards.inline.adminka.globals.select_category import new_product_select_func
from keyboards.inline.adminka.order_management_buttons.callback_datas import order_management_callback
from keyboards.inline.adminka.order_management_buttons.order_managment_buttons import order_management
from loader import dp
from states.admin_panel.order_management.delete_order_state import DeleteOrderAdmin
from states.admin_panel.order_management.edit_order_state import EditOrderAdmin


@dp.message_handler(text="😎 Управление заказами 😎")
async def get_storage_func(message: types.Message):
    await message.answer("😎 Управление заказами 😎", reply_markup=order_management)


@dp.callback_query_handler(order_management_callback.filter(type_command="order_managment_admin"))
async def order_managment_admin_call(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)

    command = callback_data.get("command")
    if command == "add":
        await call.message.answer("Выбери категорию:", reply_markup=await new_product_select_func(switch="new_order"))
    elif command == "check":
        await show_orders_func(call.message)
    elif command == "send":
        await send_orders_func(call.message)
    elif command == "delete":
        await DeleteOrderAdmin.delete_for_id.set()
        await call.message.answer("Номер заказа?")
    elif command == "edit":
        await EditOrderAdmin.edit_for_id.set()
        await call.message.answer("Номер заказа?")
