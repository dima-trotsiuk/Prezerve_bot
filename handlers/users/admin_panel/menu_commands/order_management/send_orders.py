from sqlalchemy import update
from utils.db_api.models import engine, Orders


async def send_orders_func(message):
    conn = engine.connect()

    flag = Orders.select().where(
        Orders.c.status == "processing"
    )
    flag = conn.execute(flag)
    flag = flag.rowcount

    if flag == 0:
        await message.answer("А что отправлять то? Заказов нету😳")
    else:
        u = update(Orders).where(
            Orders.c.status == "processing"
        ).values(status="completed")
        conn.execute(u)

        await message.answer(f"Все заказы ({flag}) обработаны👍")

    conn.close()
