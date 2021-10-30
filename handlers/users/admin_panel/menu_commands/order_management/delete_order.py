from aiogram.dispatcher import FSMContext
from sqlalchemy import update, delete
from aiogram import types
from loader import dp
from states.admin_panel.order_management.delete_order_state import DeleteOrderAdmin
from utils.db_api.models import engine, Orders, Order_products


@dp.message_handler(state=DeleteOrderAdmin.delete_for_id)
async def delete_order_func(message: types.Message, state: FSMContext):
    delete_id = message.text
    if delete_id.isdigit():
        conn = engine.connect()

        flag = Orders.select().where(
            Orders.c.id == delete_id
        )
        flag = conn.execute(flag)
        flag = flag.rowcount

        if flag == 0:
            await message.answer("Данного заказа не существует")
            await state.finish()
        else:

            d = delete(Order_products).where(
                Order_products.c.order_id == delete_id
            )

            conn.execute(d)

            d = delete(Orders).where(
                Orders.c.id == delete_id
            )

            conn.execute(d)
            conn.close()
            await state.finish()
            await message.answer(f"Заказ {delete_id} был удалён👌")
    else:
        await message.answer("Введи номер заказа!")


