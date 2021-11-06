from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy import and_

from handlers.users.user_panel.catalog.get_products_for_cat import get_poducts_for_cat_func
from keyboards.inline.adminka.globals.callback_datas import select_category_callback
from keyboards.inline.user.catalog.callback_datas import show_products_callback
from loader import dp
from states.user.catalog.show_product_state import ShowProduct
from utils.db_api.models import engine, Order_products
from keyboards.inline.user.catalog.show_products import show_products_button


@dp.callback_query_handler(select_category_callback.filter(type_command="user_select_category_admin"))
async def select_category_user_call(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)

    category_id = callback_data.get("category_id")

    await show_products_button(message=call.message,
                               category_id=category_id)


@dp.callback_query_handler(show_products_callback.filter(type_command="show_products_user"))
async def command_processing_catalog(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=1)

    await state.update_data(message=call.message)
    command = callback_data.get("command")
    category_id = callback_data.get("category_id")
    index_product = int(callback_data.get("index_product"))

    products_info = await get_poducts_for_cat_func(category_id)

    if command == "bag":
        product_info = products_info[index_product - 1]
        id = product_info[0]
        quantity = product_info[3]

        conn = engine.connect()
        flag = Order_products.select().where(
            and_(
                Order_products.c.product_id == id,
                Order_products.c.user_telegram_id == call.message.chat.id,
                Order_products.c.order_id == 0
                 )
            )
        flag = conn.execute(flag)
        flag = flag.rowcount
        conn.close()

        if not flag:
            if int(quantity) == 0:
                await call.message.answer(
                    f"Этого товара нету в наличии, можете уточнить дату поступления в instagram 😊")
            else:
                await ShowProduct.quantity.set()
                await state.update_data(product_info=product_info)
                await call.message.answer("Сколько штучек? 🥺")
        else:
            await call.message.answer(f"Данный товар уже в корзине 😌")

    elif command == "previous":
        if index_product == 1:
            full_index = len(products_info)
            await show_products_button(message=call.message,
                                       index_product=full_index,
                                       update=True,
                                       category_id=category_id)
        else:
            await show_products_button(message=call.message,
                                       index_product=index_product - 1,
                                       update=True,
                                       category_id=category_id)

    elif command == "next":
        if index_product == len(products_info):
            await show_products_button(message=call.message,
                                       index_product=1,
                                       update=True,
                                       category_id=category_id)
        else:
            await show_products_button(message=call.message,
                                       index_product=index_product + 1,
                                       update=True,
                                       category_id=category_id)


@dp.message_handler(state=ShowProduct.quantity)
async def answer_other(message: types.Message, state: FSMContext):
    quantity_user = message.text

    data = await state.get_data()
    product_info = data.get("product_info")

    product_id = product_info[0]
    quantity = product_info[3]
    category_id = product_info[4]

    if quantity_user.isdigit():
        """
        Если надо сбросить только состояние, воспользуйтесь await state.reset_state(with_data=False)
        """
        await state.finish()
        if quantity == 0:
            await message.reply(f"Этого товара нету в наличии, можете уточнить дату поступления в instagram 😊")

        elif int(quantity_user) <= quantity:
            conn = engine.connect()
            ins = Order_products.insert().values(
                category_id=category_id,
                product_id=product_id,
                order_id=0,
                quantity=quantity_user,
                user_telegram_id=message.chat.id
            )
            conn.execute(ins)
            await message.reply(f"Добавлено в корзину 🛒")

        else:
            await message.reply(f"На складе есть только {quantity}шт 😥")
    else:
        await message.answer(f"Введите целое число!")