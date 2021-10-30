from sqlalchemy import update
from utils.db_api.models import engine, Orders


async def send_orders_func(message):
    conn = engine.connect()

    u = update(Orders).where(
        Orders.c.status == "processing"
    ).values(status="completed")
    conn.execute(u)

    await message.answer("Все заказы обработаны👍")

    conn.close()
