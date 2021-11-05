from handlers.users.user_panel.bag.is_empty_bag import is_empty_bag_func
from utils.db_api.models import engine, Order_products


async def clear_bag(message):

    conn = engine.connect()

    conn.execute(Order_products.delete().where(Order_products.c.user_telegram_id == message.chat.id))
    conn.close()
    await message.answer("Корзина была очищена.")
    await message.delete()