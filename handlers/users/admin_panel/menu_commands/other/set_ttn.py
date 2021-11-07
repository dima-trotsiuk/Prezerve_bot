from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy import update, select, and_

from keyboards.default import admin_menu
from keyboards.default.cancel import cancel_button
from keyboards.inline.user.bag.callback_datas import message_to_admin_callback
from loader import dp, bot
from states.other.set_ttn_state import SetTtn
from utils.db_api.models import engine, Orders, Order_products, Storage


@dp.callback_query_handler(
    message_to_admin_callback.filter(type_command="set_ttn_admin"))
async def answer_category_id(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    order_id = callback_data.get("order_id")

    await state.update_data(order_id=order_id)
    await call.message.answer("Жду ТТН 😋", reply_markup=cancel_button)
    await SetTtn.set_ttn.set()
    await call.message.delete()


@dp.message_handler(text="Отмена", state=SetTtn.set_ttn)
async def share_number_func(message: types.Message, state: FSMContext):
    await message.answer("Хорошо :)", reply_markup=admin_menu)
    await state.finish()


@dp.message_handler(state=SetTtn.set_ttn)
async def button_content(message: types.Message, state: FSMContext):
    ttn = message.text
    data = await state.get_data()
    await state.finish()
    order_id = data.get("order_id")
    await writing_ttn_to_database(message=message, ttn=ttn, order_id=order_id)


async def writing_ttn_to_database(message, ttn, order_id):
    conn = engine.connect()
    conn.execute(update(Orders).where(
        Orders.c.id == order_id
    ).values(
        ttn=ttn
    ))
    conn.close()

    await message.answer(f"Заказу <b>№ {order_id}</b> был присвоен ТТН - <i>{ttn}</i>", reply_markup=admin_menu)
    await show_ttn_to_user(order_id)


async def show_ttn_to_user(order_id):
    conn = engine.connect()

    message_id = conn.execute(select([
        Orders.c.user_telegram_id
    ]).select_from(Orders).where(
        Orders.c.id == order_id
    ))
    message_id = message_id.first()[0]

    order = conn.execute(select([
        Orders.c.id,
        Orders.c.price,
        Orders.c.date,
        Orders.c.ttn
    ]).select_from(Orders.join(Order_products)).where(
        and_(
            Order_products.c.order_id == order_id,
        )))
    order = order.first()

    order_id = order[0]
    full_price = order[1]
    date = order[2]
    ttn = order[3]
    text = f"Вашему заказу был присвоен ТТН: <i>{ttn}</i>\n\n"
    text += f"<b>Заказ № {order_id}</b>\n\n"
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
        Order_products.c.user_telegram_id == message_id,
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
    await bot.send_message(message_id, text)
