from aiogram import types
from loader import dp

from aiogram.dispatcher import FSMContext
from sqlalchemy import update, delete, select
from aiogram import types
from loader import dp
from states.admin_panel.search_for_ttn.search_for_ttn_state import SearchForTtnAdmin
from utils.db_api.models import engine, Orders, Order_products, Storage


@dp.message_handler(text="Поиск по ТТН 🗿")
async def get_storage_func(message: types.Message):
    await SearchForTtnAdmin.search_for_ttn.set()
    await message.answer("ТТН заказа?")


@dp.message_handler(state=SearchForTtnAdmin.search_for_ttn)
async def delete_order_func(message: types.Message, state: FSMContext):
    ttn = message.text
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
    ]).where(Orders.c.ttn == ttn)
    info_orders = conn.execute(info_orders)
    info_orders = info_orders.fetchall()

    if not info_orders:
        await message.answer("Заказа с таким ТТН нету🗿")
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
                Storage.c.title,
            ]).select_from(
                Order_products.join(Storage)
            ).where(Order_products.c.order_id == order_id)
            rs = conn.execute(joins)  # [(50, 12, 'Лучші')]
            conn.close()
            list_products = rs.fetchall()

            result = f"<i>{date}</i>\n" \
                     f"<b>Заказ №{order_id}</b> <i>({platform})</i>\n\n" \
                     f"ТТН <i>{ttn}</i>\n"

            for into in list_products:
                quantity = into[0]
                title = into[1]

                result += f"{title}\n" \
                          f"<b>Количество: {quantity}шт</b>\n\n"

            result += f"= <b>{full_price} грн</b>"

            await message.answer(result)
        conn.close()
    await state.finish()
