from sqlalchemy import select
from utils.db_api.models import engine, Storage, Order_products, Orders


async def show_orders_func(message):
    conn = engine.connect()

    '''
    Ищем order_id, platform, full_price, date последнего заказа сделаного админом
    '''
    info_orders = select([
        Orders.c.id,
        Orders.c.platform,
        Orders.c.price,
        Orders.c.date,
        Orders.c.ttn,
    ]).where(Orders.c.status == "processing")
    info_orders = conn.execute(info_orders)
    info_orders = info_orders.fetchall()

    if not info_orders:
        await message.answer("Заказов нет😭")
    else:
        for order in info_orders:

            order_id = order[0]
            platform = order[1]
            full_price = order[2]
            date = order[3]
            ttn = order[4]

            '''
            Объединяем таблцы Order_products и Storage по номеру заказа
            '''

            joins = select([
                Order_products.c.quantity,
                Storage.c.price,
                Storage.c.title,
            ]).select_from(
                Order_products.join(Storage)
            ).where(Order_products.c.order_id == order_id)
            rs = conn.execute(joins)  # [(50, 12, 'Лучші')]

            list_products = rs.fetchall()

            '''
            Выводим данные о заказе админу
            '''

            result = f"{date}\n" \
                     f"Заказ №{order_id} ({platform})\n" \
                     f"ТТН {ttn}\n"

            for into in list_products:
                quantity = into[0]
                price = into[1]
                title = into[2]

                result += f"{title} - {quantity}шт ({price}грн)\n"

            result += f"= {full_price} грн"

            await message.answer(result)
        conn.close()
