from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.db_api.select_storage import select_storage_func
from .callback_datas import edit_storage_callback


async def show_storage_func():
    products = select_storage_func()
    list_buttons = []
    for product in products:
        id_product = product[0]
        title = product[1]

        list_button = [
            InlineKeyboardButton(
                text=f"{title}",
                callback_data=edit_storage_callback.new(id=id_product,
                                                        type_command="edit_storage_admin")
            ),
        ]
        list_buttons.append(list_button)
    list_button = [
        InlineKeyboardButton(
            text=f"+",
            callback_data=edit_storage_callback.new(id="new_product",
                                                    type_command="edit_storage_admin")
        ),
    ]
    list_buttons.append(list_button)

    return InlineKeyboardMarkup(row_width=1, inline_keyboard=list_buttons)
