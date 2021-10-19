from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .callback_datas import new_product_select_category_callback
from utils.db_api.sqlalchemy import engine, categories

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
            callback_data=new_product_select_category_callback.new(category_id=id,
                                                                   type_command="new_product_select_category_admin")
        ),
    ]
    list_buttons.append(list_button)

new_product_select_category = InlineKeyboardMarkup(row_width=1, inline_keyboard=list_buttons)
