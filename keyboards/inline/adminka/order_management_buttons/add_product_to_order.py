from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto

from .callback_datas import add_product_to_order_callback
from loader import bot

from utils.db_api.models import engine, Storage


async def add_product_to_order(product_id, message, update=False, quantity_selected=0):
    conn = engine.connect()
    product_info = Storage.select().where(Storage.c.id == product_id)
    product_info = conn.execute(product_info)
    product_info = product_info.fetchone()
    conn.close()

    title = product_info[1]
    content = product_info[2]
    quantity = product_info[3]
    price = product_info[5]
    photo = product_info[6]

    type_command = "add_pr_ord_admin"

    list_button = [
        [
            InlineKeyboardButton(
                text=f"+1",
                callback_data=add_product_to_order_callback.new(command="plus",
                                                                product_id=product_id,
                                                                quantity_selected=quantity_selected,
                                                                type_command=type_command)
            ),
            InlineKeyboardButton(
                text=f"Новое значение",
                callback_data=add_product_to_order_callback.new(command="own_value",
                                                                product_id=product_id,
                                                                quantity_selected=quantity_selected,
                                                                type_command=type_command)
            ),
            InlineKeyboardButton(
                text=f"-1",
                callback_data=add_product_to_order_callback.new(command="minus",
                                                                product_id=product_id,
                                                                quantity_selected=quantity_selected,
                                                                type_command=type_command)
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"✅ Добавить к заказу ✅",
                callback_data=add_product_to_order_callback.new(command="add_to_orders",
                                                                product_id=product_id,
                                                                quantity_selected=quantity_selected,
                                                                type_command=type_command)
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"❌ Закрыть ❌",
                callback_data=add_product_to_order_callback.new(command="close",
                                                                product_id=product_id,
                                                                quantity_selected=quantity_selected,
                                                                type_command=type_command)
            ),
        ]
    ]

    edit_product_for_id_key = InlineKeyboardMarkup(row_width=1, inline_keyboard=list_button)

    if update:
        file = InputMediaPhoto(media=photo,
                               caption=f'title - {title}\n'
                                       f'content - {content}\n'
                                       f'quantity_selected - {quantity_selected}шт ({quantity}шт)\n'
                                       f'price - {price}грн')

        await message.edit_media(file, reply_markup=edit_product_for_id_key)
    else:

        await bot.send_photo(
            chat_id=message.chat.id,
            photo=photo,
            reply_markup=edit_product_for_id_key,
            caption=f'title - {title}\n'
                    f'content - {content}\n'
                    f'quantity_selected - {quantity_selected}шт ({quantity}шт)\n'
                    f'price - {price}грн',
        )
