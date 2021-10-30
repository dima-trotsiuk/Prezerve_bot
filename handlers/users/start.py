from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart  # стандартные фильтры

from loader import dp
from utils.misc import rate_limit
from utils.db_api.models import Users, engine, Storage
import logging


@rate_limit(limit=10)
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):

    '''
    Записываем пользователей в БД
    '''
    conn = engine.connect()
    s = Users.select().where(Users.c.telegram_id == message.from_user.id)
    flag = conn.execute(s)
    flag = flag.fetchone()
    if not flag:
        ins = Users.insert().values(
            first_name=message.from_user.first_name,
            username=message.from_user.username,
            telegram_id=message.from_user.id
        )
        conn.execute(ins)

    conn.close()
    await message.answer(f'Привет, {message.from_user.full_name}!')
