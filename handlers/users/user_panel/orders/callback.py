from aiogram import types
from sqlalchemy import select, and_

from loader import dp
from utils.db_api.models import engine, Orders, Order_products, Storage


@dp.message_handler(text="Заказы 📜")
async def get_storage_func(message: types.Message):
    await show_orders_to_user(message)


async def show_orders_to_user(message):
    conn = engine.connect()

    orders = conn.execute(select([
        Orders.c.id,
        Orders.c.price,
        Orders.c.date,
    ]).select_from(Orders).where(
        and_(
            Orders.c.user_telegram_id == message.chat.id,
            Orders.c.price > 0,
        )
    ))
    orders = orders.fetchall()

    if not orders:
        await message.answer("У вас еще нету заказов 😑")
    else:
        for order in orders:
            order_id = order[0]
            full_price = order[1]
            date = order[2]
            text = f"<b>Заказ № {order_id}</b>\n\n"
            text += f"<b>Дата - </b><i>{date}\n\n</i>"

            joins = select([
                Order_products.c.id,
                Order_products.c.category_id,
                Order_products.c.product_id,
                Order_products.c.quantity,
                Storage.c.title,
                Storage.c.quantity,
                Storage.c.price,
            ]).select_from(
                Order_products.join(Storage)
            ).where(and_(
                Order_products.c.user_telegram_id == message.chat.id,
                Order_products.c.order_id == order_id))
            joins = conn.execute(joins)
            joins = joins.fetchall()

            for el in joins:
                title_product = el[4]
                quantity_in_order = el[3]
                price = el[6]
                text += f"<b>{title_product}</b>"
                price_product = int(quantity_in_order) * int(price)
                text += f"\n{quantity_in_order}шт * {price}грн = {price_product}грн\n\n"
            text += f"\n<b>Итого: {full_price}грн</b>"
            await message.answer(text)
