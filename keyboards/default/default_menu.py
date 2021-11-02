from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

default_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Каталог 🏷"),
            KeyboardButton(text="Корзина 🛒"),
        ],
        [
            KeyboardButton(text="Заказы 📜"),
            KeyboardButton(text="Доставка и оплата 💳")
        ],
        [
            KeyboardButton(text="Контакты ✉"),
        ],
    ],
    resize_keyboard=True

)
