from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline.adminka.globals.callback_datas import select_category_callback
from keyboards.inline.adminka.globals.select_category import new_product_select_func
from keyboards.inline.user.catalog.callback_datas import show_products_callback
from loader import dp
from utils.db_api.models import engine, Storage
from keyboards.inline.user.catalog.show_products import show_products_button


@dp.callback_query_handler(select_category_callback.filter(type_command="user_select_category_admin"))
async def select_category_user_call(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)

    category_id = callback_data.get("category_id")

    conn = engine.connect()
    products_info = Storage.select().where(Storage.c.category_id == category_id)
    products_info = conn.execute(products_info)
    products_info = products_info.fetchall()

    conn.close()

    await state.update_data(products_info=products_info)

    await show_products_button(product_info=products_info[0],
                               full_products=len(products_info),
                               message=call.message)


@dp.callback_query_handler(show_products_callback.filter(type_command="show_products_user"))
async def command_processing_catalog(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=1)

    command = callback_data.get("command")
    index_product = int(callback_data.get("index_product"))

    data = await state.get_data()
    products_info = data.get("products_info")

    if command == "bag":
        await call.message.answer("В разработке.")

    elif command == "previous":
        if index_product == 1:
            index_product = len(products_info)
            await show_products_button(product_info=products_info[index_product-1],
                                       full_products=index_product,
                                       message=call.message,
                                       index_product=index_product,
                                       update=True)
        else:
            await show_products_button(product_info=products_info[index_product-2],
                                       full_products=len(products_info),
                                       message=call.message,
                                       index_product=index_product - 1,
                                       update=True)

    elif command == "next":
        if index_product == len(products_info):
            index_product = 1
            await show_products_button(product_info=products_info[0],
                                       full_products=len(products_info),
                                       message=call.message,
                                       index_product=index_product,
                                       update=True)
        else:
            await show_products_button(product_info=products_info[index_product],
                                       full_products=len(products_info),
                                       message=call.message,
                                       index_product=index_product + 1,
                                       update=True)


