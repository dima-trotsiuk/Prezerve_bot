from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .callback_datas import show_buttons_callback

list_button = [
    [
        InlineKeyboardButton(
            text="Редактировать ✏️",
            callback_data=show_buttons_callback.new(command="edit",
                                                    type_command="show_buttons_bag")
        ),
        InlineKeyboardButton(
            text="Очистить ❌",
            callback_data=show_buttons_callback.new(command="clear",
                                                    type_command="show_buttons_bag")
        ),
    ],
    [
        InlineKeyboardButton(
            text="Промокод 🎁",
            callback_data=show_buttons_callback.new(command="promo_code",
                                                    type_command="show_buttons_bag")
        ),
    ],
    [
        InlineKeyboardButton(
            text="Оформить заказ ✅",
            callback_data=show_buttons_callback.new(command="checkout",
                                                    type_command="show_buttons_bag")
        ),
    ],
]

show_buttons_bag = InlineKeyboardMarkup(row_width=2, inline_keyboard=list_button)
