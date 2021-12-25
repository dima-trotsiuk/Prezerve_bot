from aiogram import types
from aiogram.dispatcher import FSMContext
from sqlalchemy import select, desc, and_, update

from handlers.users.user_panel.bag.products_in_bag import products_in_bag_func
from keyboards.default.default_menu import default_menu
from keyboards.default.get_number_bag import get_contact_keyboard
from keyboards.inline.user.bag.message_to_admin import message_to_admin_button
from loader import dp
from states.user.bag.get_namber_state import GetNumber
from utils.db_api.models import engine, Orders, Order_products, Storage, Users


async def validation(message):
    flag = True
    products_in_bag = await products_in_bag_func(message)
    for product_in_bag in products_in_bag:
        quantity_in_bag = int(product_in_bag[1])
        quantity_all = int(product_in_bag[3])

        # проверяем, доступен ли товар

        if quantity_all == 0 or quantity_in_bag > quantity_all:
            flag = False
            await message.answer("Отредактируйте корзину перед тем, как сделать заказ 😡")
            break
    if flag:
        await message.answer("Поделитесь с нами вашем номером телефона, чтобы мы могли связатся с вами. "
                             "Или напишите его ниже в формате 380661112233", reply_markup=get_contact_keyboard)
        await GetNumber.number.set()


async def writing_number_to_database(message, number):
    conn = engine.connect()
    conn.execute(update(Users).where(
        Users.c.telegram_id == message.chat.id,
    ).values(
        number=number
    ))
    conn.close()

    await checkout(message)


@dp.message_handler(text="Отмена", state=GetNumber.number)
async def share_number_func(message: types.Message, state: FSMContext):
    await message.answer("Хорошо :)", reply_markup=default_menu)
    await state.finish()


@dp.message_handler(content_types=["contact"], state=GetNumber.number)
async def button_content(message: types.Message, state: FSMContext):
    text = message.contact.phone_number

    await writing_number_to_database(message=message, number=text)
    await state.finish()


@dp.message_handler(state=GetNumber.number)
async def manual_input(message: types.Message, state: FSMContext):
    text = message.text
    if len(text) == 12:
        await writing_number_to_database(message=message, number=text)
        await state.finish()
    else:
        await message.answer("Введите номер телефона в формате +380661112233")


async def checkout(message):
    conn = engine.connect()
    conn.execute(Orders.insert().values(
        platform='telegram',
        user_telegram_id=message.chat.id
    ))

    order_id = select([
        Orders.c.id,
    ]).where(Orders.c.user_telegram_id == message.chat.id).order_by(desc(Orders.c.id)).limit(1)
    order_id = conn.execute(order_id).first()[0]

    conn.execute(update(Order_products).where(
        and_(
            Order_products.c.user_telegram_id == message.chat.id,
            Order_products.c.order_id == 1
        )
    ).values(
        order_id=order_id
    ))

    joins = select([
        Order_products.c.id,
        Order_products.c.category_id,
        Order_products.c.product_id,
        Order_products.c.quantity,
        Storage.c.title,
        Storage.c.quantity,
        Storage.c.price,
        Storage.c.photo_id,
    ]).select_from(
        Order_products.join(Storage)
    ).where(and_(
        Order_products.c.user_telegram_id == message.chat.id,
        Order_products.c.order_id == order_id
    )
    )
    rs = conn.execute(joins)
    products_in_bag = rs.fetchall()
    """
    id_order_products = [0]
    category_id = [1]
    product_id = [2]
    quantity_in_bag = [3]
    title_product = [4]
    quantity_all = [5]
    price = [6]
    photo_id = [7]
    """
    sum_price = 0
    text = f"<b>Заказ № {order_id}</b>\n\n"
    for product_in_bag in products_in_bag:

        id_order_products = product_in_bag[0]
        category_id = product_in_bag[1]
        product_id = product_in_bag[2]
        quantity_in_bag = product_in_bag[3]
        title_product = product_in_bag[4]
        quantity_all = product_in_bag[5]
        price = product_in_bag[6]
        photo_id = product_in_bag[7]
        text += f"<b>{title_product}</b>"

        # проверяем, доступен ли товар
        if quantity_all == 0:
            text += " - Товар временно недоступен ❌\n\n"
        elif quantity_in_bag > quantity_all:
            text += f" - Доступно только {quantity_all}шт. Измените количество 🥺\n\n"
        else:
            price_product = int(quantity_in_bag) * int(price)
            sum_price += price_product
            text += f"\n{quantity_in_bag}шт * {price}грн = {price_product}грн\n\n"

            conn.execute(update(Storage).where(Storage.c.id == product_id).values(
                quantity=Storage.c.quantity - quantity_in_bag
            ))

    conn.execute(update(Orders).where(Orders.c.id == order_id).values(
        price=sum_price
    ))
    conn.close()
    text += f"\n<b>Итого: {sum_price}грн</b>"
    await message.answer(text, reply_markup=default_menu)
    await sending_to_admin(message, order_id)



async def sending_to_admin(message, order_id):
    conn = engine.connect()

    '''
    Ищем order_id, platform, full_price, date заказа по id_order
    '''
    info_order = select([
        Orders.c.platform,
        Orders.c.price,
        Orders.c.date
    ]).where(Orders.c.id == order_id).order_by(desc(Orders.c.id)).limit(1)
    info_order = conn.execute(info_order)
    info_order = info_order.first()

    platform = info_order[0]
    full_price = info_order[1]
    date = info_order[2]

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

    list_products = rs.fetchall()

    '''
    Ищем номер телефона
    '''
    number_username = conn.execute(select([
        Users.c.number,
        Users.c.username
    ]).where(Users.c.telegram_id == message.chat.id))

    number = number_username.first()[0]
    username = number_username.first()[1]
    conn.close()

    '''
    Выводим данные о заказе админу
    '''

    result = f"<b>Заказ №{order_id}</b>\n\n" \
             f"<b>Дата - </b><i>{date}</i>\n" \
             f"<b>Номер телефона </b><i>{number}</i>\n\n" \
             f"<b>Юзернейм </b><i>{username}</i>\n\n"

    for into in list_products:
        quantity = into[0]
        title = into[1]

        result += f"<b>{title}</b>\n" \
                  f"Колво - {quantity}шт\n"

    result += f"\n<b>Сума: {full_price}грн</b>"
    from data import config
    for admin_id in config.admins:
        await message_to_admin_button(order_id=order_id,
                                      text=result,
                                      admin_id=admin_id)
