from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy import update
from aiogram import types

from keyboards.default import admin_menu
from keyboards.default.cancel import cancel_button
from keyboards.inline.adminka.edit_storage_buttons.edit_product import edit_product_for_id
from states.admin_panel.edit_storage.own_value_state import NewValueQuantity, NewValueOther
from utils.db_api.models import engine, Storage
from keyboards.inline.adminka.edit_storage_buttons.callback_datas import product_info_for_id_callback
from loader import dp, bot


@dp.callback_query_handler(product_info_for_id_callback.filter(type_command="edit_product_for_id_admin"))
async def edit_product_for_id_call(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer()
    product_id = callback_data.get("product_id")
    conn = engine.connect()

    if callback_data.get("command") == "plus":
        update_quantity = update(Storage).where(
            Storage.c.id == product_id
        ).values(
            quantity=Storage.c.quantity + 1,
        )
        conn.execute(update_quantity)
        await edit_product_for_id(product_id, call.message, True)

    elif callback_data.get("command") == "minus":
        update_quantity = update(Storage).where(
            Storage.c.id == product_id
        ).values(
            quantity=Storage.c.quantity - 1,
        )
        conn.execute(update_quantity)
        await edit_product_for_id(product_id, call.message, True)

    elif callback_data.get("command") == "own_value":
        await call.message.answer("Новое количество:", reply_markup=cancel_button)
        await state.update_data(product_id=product_id)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await NewValueQuantity.new_value.set()

    elif callback_data.get("command") == "other":
        await call.message.answer(f"1. Изменить заголовок\n"
                                  f"2. Изменить описание\n"
                                  f"3. Изменить фото\n"
                                  f"4. Изменить цену\n", reply_markup=cancel_button)

        await state.update_data(product_id=product_id)
        await NewValueOther.new_value_other.set()
        await bot.delete_message(call.message.chat.id, call.message.message_id)

    elif callback_data.get("command") == "close":
        await bot.delete_message(call.message.chat.id, call.message.message_id)

    conn.close()


@dp.message_handler(text="Отмена", state=NewValueQuantity.new_value)
async def share_number_func(message: types.Message, state: FSMContext):
    await message.answer("Хорошо :)", reply_markup=admin_menu)
    await state.finish()


@dp.message_handler(text="Отмена", state=NewValueOther.new_value_other)
async def share_number_func(message: types.Message, state: FSMContext):
    await message.answer("Хорошо :)", reply_markup=admin_menu)
    await state.finish()


@dp.message_handler(state=NewValueQuantity.new_value)
async def answer_quantity(message: types.Message, state: FSMContext):
    quantity = message.text
    if quantity.isdigit():
        await message.reply("Спс", reply_markup=admin_menu)

        data = await state.get_data()
        product_id = data.get("product_id")

        conn = engine.connect()
        update_quantity = update(Storage).where(
            Storage.c.id == product_id
        ).values(
            quantity=quantity,
        )
        conn.execute(update_quantity)
        conn.close()
        await state.finish()

        await edit_product_for_id(product_id, message)

    else:
        await message.answer(f"Число, мисье:")


@dp.message_handler(state=NewValueOther.new_value_other)
async def answer_other(message: types.Message, state: FSMContext):
    switch = message.text

    if switch == "1":
        await message.answer("Новый заголовок:")
        await state.update_data(command="new_title")
    elif switch == "2":
        await message.answer("Новое описание:")
        await state.update_data(command="new_content")
    elif switch == "3":
        await message.answer("Новое фото:")
        await state.update_data(command="new_photo")
    elif switch == "4":
        await message.answer("Новая цена:")
        await state.update_data(command="new_price")
    if switch in ("1", "2", "3", "4", "5"):
        await NewValueOther.info.set()
    else:
        await message.answer("Не знаю, что ты хочешь")


@dp.message_handler(text="Отмена", state=NewValueOther.info)
async def share_number_func(message: types.Message, state: FSMContext):
    await message.answer("Хорошо :)", reply_markup=admin_menu)
    await state.finish()


@dp.message_handler(state=NewValueOther.info, content_types=['photo', 'text'])
async def answer_q1(message: types.Message, state: FSMContext):
    data = await state.get_data()
    command = data.get("command")
    product_id = data.get("product_id")

    text = message.text

    conn = engine.connect()

    if command == "new_title":
        update_title = update(Storage).where(
            Storage.c.id == product_id
        ).values(
            title=text,
        )
        conn.execute(update_title)

    elif command == "new_content":
        update_content = update(Storage).where(
            Storage.c.id == product_id
        ).values(
            content=text,
        )
        conn.execute(update_content)
    elif command == "new_photo":

        # перезаписываем в бд
        document_id = message.photo[-1].file_id
        update_photo = update(Storage).where(
            Storage.c.id == product_id
        ).values(
            photo_id=document_id,
        )
        conn.execute(update_photo)
    elif command == "new_price":
        if text.isdigit():
            update_content = update(Storage).where(
                Storage.c.id == product_id
            ).values(
                price=text,
            )
            conn.execute(update_content)

    conn.close()

    await state.finish()
    await edit_product_for_id(product_id, message)
