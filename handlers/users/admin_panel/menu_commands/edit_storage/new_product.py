from aiogram.types import CallbackQuery
from aiogram.dispatcher.storage import FSMContext

from keyboards.inline.adminka.globals.callback_datas import select_category_callback
from loader import dp, bot
from aiogram import types
from states.admin_panel.edit_storage.new_product_state import NewProduct
# sqlalchemy
from utils.db_api.models import engine, storage

import logging


@dp.callback_query_handler(
    select_category_callback.filter(type_command="new_product_select_category_admin"))
async def answer_category_id(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    category_id = callback_data.get("category_id")
    await state.update_data(category_id=category_id)
    await call.message.answer("Название?")
    await NewProduct.title.set()
    await bot.delete_message(call.message.chat.id, call.message.message_id)


@dp.message_handler(state=NewProduct.title)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(title=answer)

    await message.answer("Жду фотку...")
    await NewProduct.photo.set()


@dp.message_handler(state=NewProduct.photo, content_types=['photo'])
async def answer_q1(message: types.Message, state: FSMContext):
    document_id = message.photo[-1].file_id

    await message.reply("Спс")

    await state.update_data(photo=document_id)

    await message.answer(f"Описание?")
    await NewProduct.content.set()


@dp.message_handler(state=NewProduct.content)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text

    await state.update_data(content=answer)
    await message.answer(f"Количество?")
    await NewProduct.quantity.set()


@dp.message_handler(state=NewProduct.quantity)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    if answer.isdigit():
        await state.update_data(quantity=answer)
        await message.answer(f"Цена?")
        await NewProduct.price.set()
    else:
        await message.answer(f"Введи число!")
        await NewProduct.quantity.set()


@dp.message_handler(state=NewProduct.price)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    if answer.isdigit():
        await state.update_data(price=answer)

        data = await state.get_data()
        title = data.get("title")
        photo = data.get("photo")
        content = data.get("content")
        quantity = data.get("quantity")
        category_id = data.get("category_id")
        price = message.text

        conn = engine.connect()
        try:
            ins = storage.insert().values(
                title=title,
                content=content,
                quantity=quantity,
                category_id=category_id,
                price=price,
                photo_id=photo
            )
            conn.execute(ins)
        except Exception as e:
            logging.error(f"Ошибка при добавлении товара {e}\n"
                          f"title - {title}\n"
                          f"photo - {photo}\n"
                          f"content - {content}\n"
                          f"quantity - {quantity}\n"
                          f"price - {price}\n"
                          f"category_id - {category_id}")

        conn.close()

        '''
        # сохраняем фотку
        file_info = await bot.get_file(photo)
        fi = file_info.file_path
        urllib.request.urlretrieve(f'https://api.telegram.org/file/bot{str(os.getenv("BOT_TOKEN"))}/{fi}',
                                   f'photos/{photo}.jpg')
        '''
        await message.answer("Товар успешно добавлен!")
        await state.finish()
    else:
        await message.answer(f"Введи число!")
        await NewProduct.price.set()
