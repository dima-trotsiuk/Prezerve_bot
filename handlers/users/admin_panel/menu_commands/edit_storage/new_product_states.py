import os
import urllib
from urllib import request

from aiogram.types import CallbackQuery
from aiogram.dispatcher.storage import FSMContext
from keyboards.inline.edit_storage_buttons.callback_datas import new_product_select_category_callback
from loader import dp, bot
from aiogram import types
from states.admin_panel.edit_storage import NewProduct


@dp.callback_query_handler(
    new_product_select_category_callback.filter(type_command="new_product_select_category_admin"))
async def answer_category_id(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    category_id = callback_data.get("category_id")
    await state.update_data(category_id=category_id)
    await call.message.answer("Название:")
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
    # скачуємо фотку
    document_id = message.photo[-1].file_id
    file_info = await bot.get_file(document_id)
    fi = file_info.file_path
    urllib.request.urlretrieve(f'https://api.telegram.org/file/bot{str(os.getenv("BOT_TOKEN"))}/{fi}',
                               f'photos/{document_id}.jpg')
    await bot.send_message(message.from_user.id, 'Спс')

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
    await state.update_data(quantity=answer)
    await message.answer(f"Цена?")
    await NewProduct.price.set()


@dp.message_handler(state=NewProduct.price)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(price=answer)

    data = await state.get_data()
    title = data.get("title")
    photo = data.get("photo")
    content = data.get("content")
    quantity = data.get("quantity")
    price = message.text

    await message.answer(f"Товар:\n"
                         f"title - {title}\n"
                         f"photo - {photo}\n"
                         f"content - {content}\n"
                         f"quantity - {quantity}\n"
                         f"price - {price}\n")
    await state.finish()
