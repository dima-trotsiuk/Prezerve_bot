from sqlalchemy import select, and_

from keyboards.inline.user.bag.show_buttons import show_buttons_bag
from utils.db_api.models import Categories, engine, Order_products, Storage


async def show_text_and_buttons(message):
    # ищем все товары в корзине пользователя
    conn = engine.connect()

    categories = conn.execute(Categories.select())

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
        Order_products.c.order_id == 1))
    rs = conn.execute(joins)
    products_in_bag = rs.fetchall()
    conn.close()
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

    list_cat_in_bag = []
    for cat in categories:
        id_cat = cat[0]
        if cat[0] not in list_cat_in_bag:
            for product_in_bag in products_in_bag:
                product_cat = product_in_bag[1]
                if product_cat == id_cat:
                    list_cat_in_bag.append(cat)
                    break
    text = f"<b>Корзина</b>\n\n"
    sum_price = 0
    for cat in list_cat_in_bag:
        id_cat = cat[0]
        text += f"<i>{cat[1]}:</i>\n"
        for product_in_bag in products_in_bag:
            product_cat_id = product_in_bag[1]
            if product_cat_id == id_cat:
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

    text += f"\n<b>Итого: {sum_price}грн</b>"
    await message.answer(text, reply_markup=show_buttons_bag)
