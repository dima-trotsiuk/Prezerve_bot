from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.adminka.globals.callback_datas import select_products_callback
from utils.db_api.select_storage import select_storage_func


async def show_storage_func(switch, category=0):
    products = select_storage_func(category)
    list_buttons = []
    for product in products:
        id_product = product[0]
        title = product[1]

        list_button = [
            InlineKeyboardButton(
                text=f"{title}",
                callback_data=select_products_callback.new(id=id_product,
                                                           type_command=f"{switch}_admin")
            ),
        ]
        list_buttons.append(list_button)
    if switch == 'edit_storage':
        list_button = [
            InlineKeyboardButton(
                text=f"+",
                callback_data=select_products_callback.new(id="new_product",
                                                           type_command=f"{switch}_admin")
            ),
        ]
        list_buttons.append(list_button)
    elif switch == 'new_order':
        list_button = [
            InlineKeyboardButton(
                text=f"🧐 Другая категория 🧐",
                callback_data=select_products_callback.new(id="other_category",
                                                           type_command=f"{switch}_admin")
            ),
        ]
        list_buttons.append(list_button)

        list_button = [
            InlineKeyboardButton(
                text=f"✅ Заказ готов ✅",
                callback_data=select_products_callback.new(id="save_order",
                                                           type_command=f"{switch}_admin")
            ),
        ]
        list_buttons.append(list_button)
    return InlineKeyboardMarkup(row_width=1, inline_keyboard=list_buttons)
