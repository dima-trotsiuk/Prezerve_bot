from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Вывести склад 🍑"),
            KeyboardButton(text="Редактировать склад 🤡"),
        ],
        [
            KeyboardButton(text="Управление заказами 😎"),
            KeyboardButton(text="Поиск по ТТН 🗿")
        ],
        [
            KeyboardButton(text="Статистика 🍌"),
        ],
    ],
    resize_keyboard=True

)
