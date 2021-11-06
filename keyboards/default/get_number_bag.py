from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

get_contact_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Поделиться номером телефона", request_contact=True),
            KeyboardButton(text="Отмена"),
        ],

    ],
    resize_keyboard=True

)
