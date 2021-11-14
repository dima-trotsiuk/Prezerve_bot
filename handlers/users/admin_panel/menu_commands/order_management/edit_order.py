from aiogram.dispatcher import FSMContext
from aiogram import types
from sqlalchemy import select, delete

from keyboards.default import admin_menu
from loader import dp
from states.admin_panel.order_management.edit_order_state import EditOrderAdmin
from utils.db_api.models import engine, Orders, Order_products, Storage


@dp.message_handler(text="Отмена", state=EditOrderAdmin.edit_for_id)
async def share_number_func(message: types.Message, state: FSMContext):
    await message.answer("Хорошо :)", reply_markup=admin_menu)
    await state.finish()


@dp.message_handler(state=EditOrderAdmin.edit_for_id)
async def delete_order_func(message: types.Message, state: FSMContext):
    id_order = message.text
    if id_order.isdigit():
        conn = engine.connect()

        flag = Orders.select().where(
            Orders.c.id == id_order
        )
        flag = conn.execute(flag)
        flag = flag.rowcount

        if flag == 0:
            await message.answer("Данного заказа не существует")
            await state.finish()
            conn.close()
        else:
            conn.close()
            await state.update_data(id_order=id_order)

            await show_order(message, id_order)
            await message.answer(f"1. Удалить заказ\n"
                                 f"2. Изменить товары")
            await EditOrderAdmin.command.set()

    else:
        await message.answer("Введи номер заказа!")
        await state.finish()


@dp.message_handler(state=EditOrderAdmin.command)
async def answer_other(message: types.Message, state: FSMContext):
    switch = message.text

    if switch == "1":
        await delete_order(message, state)
    elif switch == "2":
        await message.answer("В разработке", reply_markup=admin_menu)

    await state.finish()


async def show_order(message, id_order):
    conn = engine.connect()
    '''
    Ищем order_id, platform, full_price, date последнего заказа сделаного админом
    '''
    info_order = select([
        Orders.c.id,
        Orders.c.platform,
        Orders.c.price,
        Orders.c.date,
        Orders.c.ttn
    ]).where(Orders.c.id == id_order)
    info_order = conn.execute(info_order)
    info_order = info_order.first()
    order_id = info_order[0]
    platform = info_order[1]
    full_price = info_order[2]
    date = info_order[3]
    ttn = info_order[4]

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

    '''
    Выводим данные о заказе админу
    '''

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


async def delete_order(message, state: FSMContext):
    conn = engine.connect()

    data = await state.get_data()
    id_order = data.get("id_order")

    conn.execute(
        delete(Order_products).where(
            Order_products.c.order_id == id_order
        ))

    conn.execute(
        delete(Orders).where(
            Orders.c.id == id_order
        ))
    conn.close()
    await message.answer("Заказ был удалён😇", reply_markup=admin_menu)
