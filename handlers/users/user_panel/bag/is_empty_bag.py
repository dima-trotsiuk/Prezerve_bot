from sqlalchemy import and_

from utils.db_api.models import engine, Order_products


async def is_empty_bag_func(message):
    conn = engine.connect()

    flag = conn.execute(Order_products.select().where(
        and_(
            Order_products.c.user_telegram_id == message.chat.id,
            Order_products.c.order_id == 1,
        )))
    conn.close()
    flag = int(flag.rowcount)
    if not flag:
        await message.answer('Корзина пуста. Добавьте товары в "Каталоге" 😇')
    return bool(flag)
