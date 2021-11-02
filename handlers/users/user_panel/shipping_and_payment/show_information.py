from aiogram import types
from loader import dp


@dp.message_handler(text="Доставка и оплата 💳")
async def get_storage_func(message: types.Message):
    text = f"Отзывы можете найти у нас на страничке Instagram:\n" \
           f"https://www.instagram.com/prezerve.ua/\n\n" \
           f"Варианты доставки:\n" \
           f"- Новая Почта\n\n" \
           f"Варианты оплаты:\n" \
           f"- Оплата на карту\n" \
           f"- Оплата при получении\n\n" \
           f"Анонимность гарантируется💪"
    await message.answer(text)