import logging

from aiogram import types
from aiogram.types import CallbackQuery
from sqlalchemy import select, asc, desc, update

from keyboards.inline.adminka.globals.callback_datas import select_category_callback, select_products_callback
from keyboards.inline.adminka.globals.select_category import new_product_select_func
from keyboards.inline.adminka.globals.show_storage import show_storage_func
from keyboards.inline.adminka.order_management_buttons.add_product_to_order import add_product_to_order
from keyboards.inline.adminka.order_management_buttons.callback_datas import add_product_to_order_callback
from loader import dp
from states.admin_panel.order_management.add_order_state import AddOrderAdmin

from utils.db_api.models import engine, Storage, Order_products, Orders
from aiogram.dispatcher import FSMContext




@dp.message_handler(state=AddOrderAdmin.set_ttn)
async def answer_q2(message: types.Message, state: FSMContext):
    ttn = message.text

    conn = engine.connect()

    '''
    Ищем order_id, platform, full_price, date последнего заказа сделаного админом
    '''
    info_order = select([
        Orders.c.id,
        Orders.c.platform,
        Orders.c.price,
        Orders.c.date
    ]).where(Orders.c.user_telegram_id == message.chat.id).order_by(desc(Orders.c.id)).limit(1)
    info_order = conn.execute(info_order)
    info_order = info_order.first()
    order_id = info_order[0]
    platform = info_order[1]
    full_price = info_order[2]
    date = info_order[3]

    '''
    Записываем ТТН в заказ
    '''

    u = update(Orders).where(
        Orders.c.id == order_id
    ).values(ttn=ttn)
    conn.execute(u)

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
    conn.close()
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

    await state.finish()
