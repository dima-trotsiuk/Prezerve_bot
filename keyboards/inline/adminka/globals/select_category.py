from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.adminka.globals.callback_datas import select_category_callback
from utils.db_api.models import engine, categories


async def new_product_select_func(switch):
    conn = engine.connect()
    categories_list = categories.select()
    categories_list = conn.execute(categories_list)
    categories_list = categories_list.fetchall()
    conn.close()

    list_buttons = []
    for cat in categories_list:
        id = cat[0]
        title = cat[1]

        list_button = [
            InlineKeyboardButton(
                text=f"{title}",
                callback_data=select_category_callback.new(category_id=id,
                                                           type_command=f"{switch}_select_category_admin")
            ),
        ]
        list_buttons.append(list_button)

    return InlineKeyboardMarkup(row_width=1, inline_keyboard=list_buttons)
