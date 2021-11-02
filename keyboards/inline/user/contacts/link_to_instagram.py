from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


link_to_instagram_button = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Instagram",
            url="https://www.instagram.com/prezerve.ua/"
        )
    ]
])
