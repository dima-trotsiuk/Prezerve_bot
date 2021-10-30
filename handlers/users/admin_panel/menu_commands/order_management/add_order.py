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


@dp.callback_query_handler(select_category_callback.filter(type_command="new_order_select_category_admin"))
async def new_order_select_category_call(call: CallbackQuery, callback_data: dict):
    await call.answer()
    category_id = callback_data.get("category_id")
    await call.message.delete()
    await call.message.answer("Выбери товары:",
                              reply_markup=await show_storage_func(switch="new_order", category=category_id))

    conn = engine.connect()
    ins = Orders.insert().values(
        platform='instagram',
        user_telegram_id=call.message.chat.id
    )
    conn.execute(ins)
    conn.close()


@dp.callback_query_handler(select_products_callback.filter(type_command="new_order_admin"))
async def new_order_call(call: CallbackQuery, callback_data: dict):
    await call.answer()

    if callback_data.get("id") == "other_category":
        await call.message.delete()
        await call.message.answer("Выбери категорию:", reply_markup=await new_product_select_func(switch="new_order"))

    elif callback_data.get("id") == "save_order":
        await call.message.delete()
        await price_set(call.message)
    else:
        product_id = callback_data.get("id")
        await add_product_to_order(product_id=product_id, message=call.message)


@dp.callback_query_handler(add_product_to_order_callback.filter(type_command="add_pr_ord_admin"))
async def add_product_to_order_call(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer()

    product_id = callback_data.get("product_id")
    quantity_selected = int(callback_data.get("quantity_selected"))
    conn = engine.connect()
    await state.update_data(product_id=product_id)
    await state.update_data(quantity_selected=quantity_selected)

    max_quantity = Storage.select().where(Storage.c.id == product_id)
    max_quantity = conn.execute(max_quantity)
    max_quantity = int(max_quantity.first()[3])

    if callback_data.get("command") == "plus":
        if quantity_selected < max_quantity:
            quantity_selected += 1
            await state.update_data(product_id=product_id)
            await state.update_data(quantity_selected=quantity_selected)
            await add_product_to_order(product_id=product_id,
                                       message=call.message,
                                       update=True,
                                       quantity_selected=quantity_selected)
        else:
            await call.message.answer(f"Ало, у тебя нету столько товара")
    elif callback_data.get("command") == "minus":
        if quantity_selected > 0:
            quantity_selected -= 1
            await state.update_data(product_id=product_id)
            await state.update_data(quantity_selected=quantity_selected)
            await add_product_to_order(product_id=product_id,
                                       message=call.message,
                                       update=True,
                                       quantity_selected=quantity_selected)
        else:
            await call.message.answer(f"Меньше нуля не могу отправить")
    elif callback_data.get("command") == "own_value":
        await AddOrderAdmin.new_value.set()
        await state.update_data(product_id=product_id)
        await state.update_data(message=call.message)
        await call.message.answer("Введи значение:")

    elif callback_data.get("command") == "close":
        await call.message.delete()
    elif callback_data.get("command") == "add_to_orders":
        category_id = select([
            Storage.c.category_id,
        ]).where(Storage.c.id == product_id)
        category_id = conn.execute(category_id)

        category_id = category_id.first()[0]

        order_id = select([
            Orders.c.id,
        ]).where(Orders.c.user_telegram_id == call.message.chat.id).order_by(desc(Orders.c.id)).limit(1)
        order_id = conn.execute(order_id)

        order_id = order_id.first()[0]

        data = await state.get_data()
        product_id = data.get('product_id')
        quantity_selected = data.get('quantity_selected')

        transaction = conn.begin()

        try:
            u = update(Storage).where(
                Storage.c.id == product_id
            ).values(quantity=Storage.c.quantity - quantity_selected)
            conn.execute(u)

            ins = Order_products.insert().values(
                category_id=category_id,
                product_id=product_id,
                order_id=order_id,
                quantity=quantity_selected,
            )
            conn.execute(ins)
            transaction.commit()
        except Exception as e:
            logging.error(f"Ошибка при добавлении товара в заказ\n"
                          f"{e}")
            transaction.rollback()
        await call.message.delete()

    conn.close()


@dp.message_handler(state=AddOrderAdmin.new_value)
async def answer_q1(message: types.Message, state: FSMContext):
    data = await state.get_data()
    product_id = data.get("product_id")
    call_message = data.get("message")
    conn = engine.connect()
    max_quantity = Storage.select().where(Storage.c.id == product_id)
    max_quantity = conn.execute(max_quantity)
    max_quantity = int(max_quantity.first()[3])
    conn.close()

    quantity_selected = message.text
    if quantity_selected.isdigit():
        quantity_selected = int(quantity_selected)
        if 0 < quantity_selected <= max_quantity:
            await state.update_data(quantity_selected=quantity_selected)
            await state.finish()

            await add_product_to_order(product_id=product_id,
                                       message=call_message,
                                       update=True,
                                       quantity_selected=quantity_selected)
        else:
            await message.answer(f"Доступно только {max_quantity}!")
    else:
        await message.answer("Введи число!")
        await AddOrderAdmin.new_value.set()


async def price_set(message):
    conn = engine.connect()
    #  проверяем на наличие товаров в заказе

    order_id = select([
        Orders.c.id,
    ]).where(Orders.c.user_telegram_id == message.chat.id).order_by(desc(Orders.c.id)).limit(1)
    order_id = conn.execute(order_id)

    order_id = order_id.first()[0]

    order_products_list = Order_products.select().where(
        Order_products.c.order_id == order_id
    )
    order_products_list = conn.execute(order_products_list)
    quantity_products = order_products_list.rowcount

    if quantity_products == 0:
        await message.answer("Сначала добавь товары в заказ")
    else:
        quantity_and_product_id = select([
            Order_products.c.quantity,
            Order_products.c.product_id,
        ]).where(Order_products.c.order_id == order_id)
        quantity_and_product_id = conn.execute(quantity_and_product_id)
        quantity_and_product_id = quantity_and_product_id.fetchall()

        sum = 0
        for q_and_p in quantity_and_product_id:
            quantity = q_and_p[0]
            product_id = q_and_p[1]

            price_product = select([
                Storage.c.price,
            ]).where(Storage.c.id == product_id)
            price_product = int((conn.execute(price_product)).first()[0])
            sum += price_product * quantity

        u = update(Orders).where(
            Orders.c.id == order_id
        ).values(price=sum)
        conn.execute(u)
        conn.close()
        await AddOrderAdmin.set_ttn.set()
        await message.answer("Жду ТТН:")


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
