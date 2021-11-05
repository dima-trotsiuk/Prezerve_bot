from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy import select, and_

from handlers.users.user_panel.bag.products_in_bag import products_in_bag_func
from keyboards.inline.user.bag.callback_datas import edit_products_in_bag_callback
from keyboards.inline.user.bag.edit_products_in_bag import edit_products_in_bag_func
from loader import dp
from states.user.bag.edit_quantity_state import EditQuantity
from utils.db_api.models import engine, Order_products, Storage


async def show_buttons_edit_bag(message, state: FSMContext):
    products_in_bag = await products_in_bag_func(message)

    await state.update_data(products_in_bag=products_in_bag)

    await edit_products_in_bag_func(product_info=products_in_bag[0],
                                    full_products=len(products_in_bag),
                                    message=message)


@dp.callback_query_handler(edit_products_in_bag_callback.filter(type_command="edit_products_bag"))
async def edit_bag_call(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=1)

    await state.update_data(message=call.message)

    command = callback_data.get("command")
    index_product = int(callback_data.get("index_product"))

    data = await state.get_data()
    products_in_bag = data.get("products_in_bag")

    if command == "edit":
        product_info = products_in_bag[index_product - 1]
        await EditQuantity.quantity.set()
        await state.update_data(product_info=product_info)
        await state.update_data(index_product=index_product)
        await call.message.answer("Сколько штучек? 🥺")

    elif command == "previous":
        if index_product == 1:
            index_product = len(products_in_bag)
            await edit_products_in_bag_func(product_info=products_in_bag[index_product - 1],
                                            full_products=index_product,
                                            message=call.message,
                                            index_product=index_product,
                                            update=True)
        else:
            await edit_products_in_bag_func(product_info=products_in_bag[index_product - 2],
                                            full_products=len(products_in_bag),
                                            message=call.message,
                                            index_product=index_product - 1,
                                            update=True)

    elif command == "next":
        if index_product == len(products_in_bag):
            index_product = 1
            await edit_products_in_bag_func(product_info=products_in_bag[0],
                                            full_products=len(products_in_bag),
                                            message=call.message,
                                            index_product=index_product,
                                            update=True)
        else:
            await edit_products_in_bag_func(product_info=products_in_bag[index_product],
                                            full_products=len(products_in_bag),
                                            message=call.message,
                                            index_product=index_product + 1,
                                            update=True)
    elif command == "finish":
        await call.message.delete()

    elif command == "delete":
        product_info = products_in_bag[index_product - 1]
        id_product_order = int(product_info[0])

        conn = engine.connect()

        conn.execute(Order_products.delete().where(
            Order_products.c.id == id_product_order
        ))
        conn.close()

        products_in_bag = await products_in_bag_func(call.message)
        await state.update_data(products_in_bag=products_in_bag)
        await call.message.delete()


@dp.message_handler(state=EditQuantity.quantity)
async def answer_other(message: types.Message, state: FSMContext):
    quantity_user = message.text

    data = await state.get_data()
    product_info = data.get("product_info")
    products_in_bag = data.get("products_in_bag")
    message_post = data.get("message")
    index_product = data.get("index_product")

    product_order_id = product_info[0]
    quantity = product_info[3]

    product_info_list = list(product_info)
    product_info_list[1] = int(quantity_user)

    if quantity_user.isdigit():
        """
        Если надо сбросить только состояние, воспользуйтесь await state.reset_state(with_data=False)
        """
        await state.reset_state(with_data=False)

        if int(quantity_user) <= quantity:
            conn = engine.connect()
            conn.execute(Order_products.update().values(
                quantity=quantity_user,
            ).where(Order_products.c.id == product_order_id))

            await edit_products_in_bag_func(product_info=product_info_list,
                                            full_products=len(products_in_bag),
                                            message=message_post,
                                            index_product=index_product,
                                            update=True)
            await message.reply("Оновлено 👌")

            # оновляем инфу
            products_in_bag = await products_in_bag_func(message)

            await state.update_data(products_in_bag=products_in_bag)

        else:
            await message.reply(f"На складе есть только {quantity}шт 😥")
    else:
        await message.answer(f"Введите целое число!")