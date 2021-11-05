from sqlalchemy import select, desc, and_, update

from utils.db_api.models import engine, Orders, Order_products, Storage


async def checkout(message):
    conn = engine.connect()
    conn.execute(Orders.insert().values(
        platform='telegram',
        user_telegram_id=message.chat.id
    ))

    order_id = select([
        Orders.c.id,
    ]).where(Orders.c.user_telegram_id == message.chat.id).order_by(desc(Orders.c.id)).limit(1)
    order_id = conn.execute(order_id).first()[0]

    conn.execute(update(Order_products).where(
        and_(
            Order_products.c.user_telegram_id == message.chat.id,
            Order_products.c.order_id == 0
        )
    ).values(
        order_id=order_id
    ))

    joins = select([
        Order_products.c.id,
        Order_products.c.category_id,
        Order_products.c.product_id,
        Order_products.c.quantity,
        Storage.c.title,
        Storage.c.quantity,
        Storage.c.price,
        Storage.c.photo_id,
    ]).select_from(
        Order_products.join(Storage)
    ).where(and_(
        Order_products.c.user_telegram_id == message.chat.id,
        Order_products.c.order_id == order_id
    )
    )
    rs = conn.execute(joins)
    products_in_bag = rs.fetchall()
    """
    id_order_products = [0]
    category_id = [1]
    product_id = [2]
    quantity_in_bag = [3]
    title_product = [4]
    quantity_all = [5]
    price = [6]
    photo_id = [7]
    """
    sum_price = 0
    text = f"<b>Заказ № {order_id}</b>\n\n"
    for product_in_bag in products_in_bag:

        id_order_products = product_in_bag[0]
        category_id = product_in_bag[1]
        product_id = product_in_bag[2]
        quantity_in_bag = product_in_bag[3]
        title_product = product_in_bag[4]
        quantity_all = product_in_bag[5]
        price = product_in_bag[6]
        photo_id = product_in_bag[7]
        text += f"<b>{title_product}</b>"

        # проверяем, доступен ли товар
        if quantity_all == 0:
            text += " - Товар временно недоступен ❌\n\n"
        elif quantity_in_bag > quantity_all:
            text += f" - Доступно только {quantity_all}шт. Измените количество 🥺\n\n"
        else:
            price_product = int(quantity_in_bag) * int(price)
            sum_price += price_product
            text += f"\n{quantity_in_bag}шт * {price}грн = {price_product}грн\n\n"

    conn.execute(update(Orders).where(Orders.c.id == order_id).values(
        price=sum_price
    ))
    text += f"\n<b>Итого: {sum_price}грн</b>"
    await message.answer(text)

    conn.close()
