from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import bot
from .callback_datas import message_to_admin_callback


async def message_to_admin_button(order_id, text, admin_id):
    list_button = [
        [
            InlineKeyboardButton(
                text="Задать ТТН",
                callback_data=message_to_admin_callback.new(order_id=order_id,
                                                            type_command="set_ttn_admin")
            ),
        ],
    ]

    message_to_admin_keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=list_button)

    await bot.send_message(admin_id, text, reply_markup=message_to_admin_keyboard)
