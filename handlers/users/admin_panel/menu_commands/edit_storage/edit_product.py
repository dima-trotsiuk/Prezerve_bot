import os
import urllib
from urllib import request
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy import update
from aiogram import types

from keyboards.inline.edit_storage_buttons.edit_product import edit_product_for_id
from states.admin_panel.edit_storage.own_value_state import NewValueQuantity, NewValueOther
from utils.db_api.models import engine, storage
from keyboards.inline.edit_storage_buttons.callback_datas import product_info_for_id_callback
from loader import dp, bot


@dp.callback_query_handler(product_info_for_id_callback.filter(type_command="edit_product_for_id_admin"))
async def edit_product_for_id_call(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer()
    product_id = callback_data.get("product_id")
    conn = engine.connect()

    if callback_data.get("command") == "plus":
        update_quantity = update(storage).where(
            storage.c.id == product_id
        ).values(
            quantity=storage.c.quantity + 1,
        )
        conn.execute(update_quantity)
        await edit_product_for_id(product_id, call.message, True)

    elif callback_data.get("command") == "minus":
        update_quantity = update(storage).where(
            storage.c.id == product_id
        ).values(
            quantity=storage.c.quantity - 1,
        )
        conn.execute(update_quantity)
        await edit_product_for_id(product_id, call.message, True)

    elif callback_data.get("command") == "own_value":
        await call.message.answer("Новое количество:")
        await state.update_data(product_id=product_id)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await NewValueQuantity.new_value.set()

    elif callback_data.get("command") == "other":
        await call.message.answer(f"1. Изменить заголовок\n"
                                  f"2. Изменить описание\n"
                                  f"3. Изменить фото\n")

        await state.update_data(product_id=product_id)
        await NewValueOther.new_value_other.set()
        await bot.delete_message(call.message.chat.id, call.message.message_id)

    elif callback_data.get("command") == "close":
        await bot.delete_message(call.message.chat.id, call.message.message_id)

    conn.close()


@dp.message_handler(state=NewValueQuantity.new_value)
async def answer_quantity(message: types.Message, state: FSMContext):
    quantity = message.text
    if quantity.isdigit():
        await message.reply("Спс")

        data = await state.get_data()
        product_id = data.get("product_id")

        conn = engine.connect()
        update_quantity = update(storage).where(
            storage.c.id == product_id
        ).values(
            quantity=quantity,
        )
        conn.execute(update_quantity)
        conn.close()
        await state.finish()

        await edit_product_for_id(product_id, message)

    else:
        await message.answer(f"Число, мисье:")
        await NewValueQuantity.new_value.set()


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
    await NewValueOther.info.set()


@dp.message_handler(state=NewValueOther.info, content_types=['photo', 'text'])
async def answer_q1(message: types.Message, state: FSMContext):
    data = await state.get_data()
    command = data.get("command")
    product_id = data.get("product_id")

    conn = engine.connect()
    if command == "new_title":
        title = message.text

        update_title = update(storage).where(
            storage.c.id == product_id
        ).values(
            title=title,
        )
        conn.execute(update_title)

    elif command == "new_content":
        content = message.text

        update_content = update(storage).where(
            storage.c.id == product_id
        ).values(
            content=content,
        )
        conn.execute(update_content)
    elif command == "new_photo":
        """
        # старый способ
        # удаляем старую фотку
        path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', 'photos', f'{photo_url}.jpg'))

        os.remove(path)

        # сохраняем новую фотку
        file_info = await bot.get_file(document_id)
        fi = file_info.file_path
        urllib.request.urlretrieve(f'https://api.telegram.org/file/bot{str(os.getenv("BOT_TOKEN"))}/{fi}',
                                   f'photos/{document_id}.jpg')
        """
        # перезаписываем в бд
        document_id = message.photo[-1].file_id
        update_photo = update(storage).where(
            storage.c.id == product_id
        ).values(
            photo_id=document_id,
        )
        conn.execute(update_photo)

    conn.close()

    await state.finish()
    await edit_product_for_id(product_id, message)
