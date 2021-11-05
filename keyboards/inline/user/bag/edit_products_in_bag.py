from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto

from loader import bot
from .callback_datas import edit_products_in_bag_callback


async def edit_products_in_bag_func(product_info, full_products, message, index_product=1, update=False):
    """
    :param update:
    :param index_product:
    :param message:
    :param full_products:
    :param product_info:

    Order_products.c.id, [0]
    Order_products.c.quantity, [1]
    Storage.c.title, [2]
    Storage.c.quantity, [3]
    Storage.c.price, [4]
    Storage.c.photo_id, [5]
    """
    quantity_in_bag = product_info[1]
    title = product_info[2]
    quantity_all = product_info[3]
    price = product_info[4]
    photo = product_info[5]

    sum_all = int(quantity_in_bag) * int(price)

    edit_button = {"text": f"✏️ {quantity_in_bag}шт", "command": "edit"}

    quantity_text = ''
    if int(quantity_all) == 0:
        edit_button["text"] = f"Удалить из корзины ❌"
        edit_button["command"] = "delete"
        quantity_text = f"\n\nЭтот товар временно недоступен."

    elif int(quantity_all) < int(quantity_in_bag):
        quantity_text = f"\n\nВ наличии только {quantity_all}шт!"

    if full_products == 1:
        list_button = [
            [
                InlineKeyboardButton(
                    text=edit_button["text"],
                    callback_data=edit_products_in_bag_callback.new(command=edit_button["command"],
                                                                    index_product=index_product,
                                                                    type_command="edit_products_bag")
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"Завершить редактирование ✅",
                    callback_data=edit_products_in_bag_callback.new(command="finish",
                                                                    index_product=index_product,
                                                                    type_command="edit_products_bag")
                )
            ]
        ]
    else:
        list_button = [
            [
                InlineKeyboardButton(
                    text=edit_button["text"],
                    callback_data=edit_products_in_bag_callback.new(command=edit_button["command"],
                                                                    index_product=index_product,
                                                                    type_command="edit_products_bag")
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"⬅️",
                    callback_data=edit_products_in_bag_callback.new(command="previous",
                                                                    index_product=index_product,
                                                                    type_command="edit_products_bag")
                ),
                InlineKeyboardButton(
                    text=f"{index_product} / {full_products}",
                    callback_data=edit_products_in_bag_callback.new(command="ignore",
                                                                    index_product=index_product,
                                                                    type_command="edit_products_bag")
                ),
                InlineKeyboardButton(
                    text=f"➡️",
                    callback_data=edit_products_in_bag_callback.new(command="next",
                                                                    index_product=index_product,
                                                                    type_command="edit_products_bag")
                ),
            ],
            [
                InlineKeyboardButton(
                    text=f"Завершить редактирование ✅",
                    callback_data=edit_products_in_bag_callback.new(command="finish",
                                                                    index_product=index_product,
                                                                    type_command="edit_products_bag")
                )
            ]
        ]

    show_buttons_bag = InlineKeyboardMarkup(row_width=2, inline_keyboard=list_button)

    if update:
        file = InputMediaPhoto(media=photo,
                               caption=f'{title}\n\n'
                                       f'{quantity_in_bag}шт * {price}грн = {sum_all}грн')

        await message.edit_media(file, reply_markup=show_buttons_bag)
    else:
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=photo,
            reply_markup=show_buttons_bag,
            caption=f"{title}\n\n"
                    f"{quantity_in_bag}шт * {price}грн = {sum_all}грн"
                    f"{quantity_text}")
