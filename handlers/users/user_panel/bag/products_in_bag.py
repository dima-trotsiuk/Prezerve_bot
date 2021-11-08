from sqlalchemy import select, and_

from utils.db_api.models import engine, Order_products, Storage


async def products_in_bag_func(message):
    conn = engine.connect()
    joins = select([
        Order_products.c.id,
        Order_products.c.quantity,
        Storage.c.title,
        Storage.c.quantity,
        Storage.c.price,
        Storage.c.photo_id,
        Storage.c.id,
    ]).select_from(
        Order_products.join(Storage)
    ).where(
        and_(
            Order_products.c.user_telegram_id == message.chat.id,
            Order_products.c.order_id == 1))
    rs = conn.execute(joins)
    conn.close()

    return rs.fetchall()
