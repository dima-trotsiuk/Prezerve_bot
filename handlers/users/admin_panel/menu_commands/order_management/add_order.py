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

from utils.db_api.models import engine, storage, order_products, orders
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(select_category_callback.filter(type_command="new_order_select_category_admin"))
async def new_order_select_category_call(call: CallbackQuery, callback_data: dict):
    await call.answer()
    category_id = callback_data.get("category_id")
    await call.message.delete()
    await call.message.answer("Выбери товары:",
                              reply_markup=await show_storage_func(switch="new_order", category=category_id))

    conn = engine.connect()
    ins = orders.insert().values(
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
        conn = engine.connect()
        #  проверяем на наличие товаров в заказе

        order_id = select([
            orders.c.id,
        ]).order_by(desc(orders.c.id)).limit(1)
        order_id = conn.execute(order_id)

        order_id = order_id.first()[0]

        order_products_list = order_products.select().where(
            order_products.c.order_id == order_id
        )
        order_products_list = conn.execute(order_products_list)
        quantity_products = order_products_list.rowcount

        if quantity_products == 0:
            await call.message.answer("Сначала добавь товары в заказ")
        else:
            await call.message.answer(f"Колво товаров - {quantity_products}")

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

    max_quantity = storage.select().where(storage.c.id == product_id)
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
            storage.c.category_id,
        ]).where(storage.c.id == product_id)
        category_id = conn.execute(category_id)

        category_id = category_id.first()[0]

        order_id = select([
            orders.c.id,
        ]).order_by(desc(orders.c.id)).limit(1)
        order_id = conn.execute(order_id)

        order_id = order_id.first()[0]

        data = await state.get_data()
        product_id = data.get('product_id')
        quantity_selected = data.get('quantity_selected')

        transaction = conn.begin()

        try:
            u = update(storage).where(
                storage.c.id == product_id
            ).values(quantity=storage.c.quantity - quantity_selected)
            conn.execute(u)

            ins = order_products.insert().values(
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
    max_quantity = storage.select().where(storage.c.id == product_id)
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
