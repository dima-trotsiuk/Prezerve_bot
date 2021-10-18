from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.storage import FSMContext
from loader import dp
from aiogram import types
from states import Test


@dp.message_handler(Command("test"))
async def enter_test(message: types.Message):
    await message.answer("Ви почали тестування. Питання номер один:!")

    await Test.Q1.set()


@dp.message_handler(state=Test.Q1)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text

    await state.update_data(otvet1=answer)

    await message.answer("Питання номер два:")

    await Test.Q2.set()


@dp.message_handler(state=Test.Q2)
async def answer_q1(message: types.Message, state: FSMContext):
    data = await state.get_data()
    data1 = data.get("otvet1")
    data2 = message.text

    await message.answer(f"Ваші відповіді: {data1}, {data2}")
    await state.finish()


