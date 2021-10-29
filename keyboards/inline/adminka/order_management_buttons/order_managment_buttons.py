from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .callback_datas import order_management_callback

order_management = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Добавить",
            callback_data=order_management_callback.new(command="add", type_command="order_managment_admin")
        ),
        InlineKeyboardButton(
            text="Посмотреть",
            callback_data=order_management_callback.new(command="check", type_command="order_managment_admin")
        )
    ],
    [
        InlineKeyboardButton(
            text="Отправить",
            callback_data=order_management_callback.new(command="send", type_command="order_managment_admin")

        ),
        InlineKeyboardButton(
            text="Редактировать",
            callback_data=order_management_callback.new(command="edit", type_command="order_managment_admin")
        ),
    ],
    [
        InlineKeyboardButton(
            text="Удалить",
            callback_data=order_management_callback.new(command="delete", type_command="order_managment_admin")
        )
    ]
])
