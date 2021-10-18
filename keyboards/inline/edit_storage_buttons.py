from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_datas import edit_storage_callback
from utils.db_api.sqlalchemy import engine, storage

conn = engine.connect()
products = storage.select()
products = conn.execute(products)
products = products.fetchall()
conn.close()

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

edit_storage = InlineKeyboardMarkup(row_width=1, inline_keyboard=list_buttons)
