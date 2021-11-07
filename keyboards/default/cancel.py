from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

cancel_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Отмена"),
        ],

    ],
    resize_keyboard=True

)
