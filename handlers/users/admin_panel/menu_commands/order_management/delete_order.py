from aiogram.dispatcher import FSMContext
from sqlalchemy import delete
from aiogram import types
from loader import dp
from states.admin_panel.order_management.delete_order_state import DeleteOrderAdmin
from utils.db_api.models import engine, Orders, Order_products, Storage


@dp.message_handler(state=DeleteOrderAdmin.delete_for_id)
async def delete_order_func(message: types.Message, state: FSMContext):
    id_order = message.text
    await state.finish()
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
        else:

            d = delete(Order_products).where(
                Order_products.c.order_id == id_order
            )

            conn.execute(d)

            d = delete(Orders).where(
                Orders.c.id == id_order
            )

            conn.execute(d)
            conn.close()

            await message.answer(f"Заказ {id_order} был удалён👌")
    else:
        await message.answer("Введи номер заказа!")
        await state.finish()


