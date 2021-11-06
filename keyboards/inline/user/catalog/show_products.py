from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto

from handlers.users.user_panel.catalog.get_products_for_cat import get_poducts_for_cat_func
from loader import bot
from .callback_datas import show_products_callback


async def show_products_button(message, category_id, index_product=1, update=False):

    products_info = await get_poducts_for_cat_func(category_id)
    product_info = products_info[index_product - 1]
    content = product_info[2]
    quantity = product_info[3]
    price = product_info[5]
    photo = product_info[6]

    full_products = len(products_info)

    if int(quantity) == 0:
        text_availability = "Нет в наличии ❌"
    else:
        text_availability = f"Доступно {quantity} шт"

    list_button = [
        [
            InlineKeyboardButton(
                text="В корзину  🛒",
                callback_data=show_products_callback.new(command="bag",
                                                         index_product=index_product,
                                                         type_command="show_products_user",
                                                         category_id=category_id)
            )
        ],
        [
            InlineKeyboardButton(
                text=f"⬅️",
                callback_data=show_products_callback.new(command="previous",
                                                         index_product=index_product,
                                                         type_command="show_products_user",
                                                         category_id=category_id)
            ),
            InlineKeyboardButton(
                text=f"{index_product} / {full_products}",
                callback_data=show_products_callback.new(command="ignore",
                                                         index_product=index_product,
                                                         type_command="show_products_user",
                                                         category_id=category_id)
            ),
            InlineKeyboardButton(
                text=f"➡️",
                callback_data=show_products_callback.new(command="next",
                                                         index_product=index_product,
                                                         type_command="show_products_user",
                                                         category_id=category_id)
            ),
        ],
        [
            InlineKeyboardButton(
                text=text_availability,
                callback_data=show_products_callback.new(command="ignore",
                                                         index_product=index_product,
                                                         type_command="show_products_user",
                                                         category_id=category_id)
            )
        ]
    ]

    show_products_buttons = InlineKeyboardMarkup(row_width=3, inline_keyboard=list_button)

    if update:
        file = InputMediaPhoto(media=photo,
                               caption=f'{content}\n\n'
                                       f'💸 {price}грн / шт')

        await message.edit_media(file, reply_markup=show_products_buttons)
    else:

        await bot.send_photo(
            chat_id=message.chat.id,
            photo=photo,
            reply_markup=show_products_buttons,
            caption=f'{content}\n\n'
                    f'💸 {price}грн / шт')
