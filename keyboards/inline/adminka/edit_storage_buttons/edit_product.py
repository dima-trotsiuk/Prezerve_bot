from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto

from loader import bot
from .callback_datas import product_info_for_id_callback
from utils.db_api.models import engine, Storage


async def edit_product_for_id(product_id, message, update=False):
    conn = engine.connect()
    product_info = Storage.select().where(Storage.c.id == product_id)
    product_info = conn.execute(product_info)
    product_info = product_info.fetchone()
    conn.close()

    title = product_info[1]
    content = product_info[2]
    quantity = product_info[3]
    price = product_info[5]
    photo = product_info[6]

    list_button = [
        [
            InlineKeyboardButton(
                text=f"+1",
                callback_data=product_info_for_id_callback.new(command="plus",
                                                               product_id=product_id,
                                                               type_command="edit_product_for_id_admin")
            ),
            InlineKeyboardButton(
                text=f"Новое значение",
                callback_data=product_info_for_id_callback.new(command="own_value",
                                                               product_id=product_id,
                                                               type_command="edit_product_for_id_admin")
            ),
            InlineKeyboardButton(
                text=f"-1",
                callback_data=product_info_for_id_callback.new(command="minus",
                                                               product_id=product_id,
                                                               type_command="edit_product_for_id_admin")
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"Изменить другие значения",
                callback_data=product_info_for_id_callback.new(command="other",
                                                               product_id=product_id,
                                                               type_command="edit_product_for_id_admin")
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"Закрыть",
                callback_data=product_info_for_id_callback.new(command="close",
                                                               product_id=product_id,
                                                               type_command="edit_product_for_id_admin")
            ),
        ]
    ]

    edit_product_for_id_key = InlineKeyboardMarkup(row_width=1, inline_keyboard=list_button)

    if update:
        '''
        # старый способ
        photo_bytes = InputFile(path_or_bytesio=f"photos/{photo}.jpg")
        '''

        file = InputMediaPhoto(media=photo,
                               caption=f'{title}\n'
                                       f'{content}\n'
                                       f'{quantity}шт\n'
                                       f'{price}грн')

        await message.edit_media(file, reply_markup=edit_product_for_id_key)
    else:

        await bot.send_photo(
            chat_id=message.chat.id,
            photo=photo,
            reply_markup=edit_product_for_id_key,
            caption=f'{title}\n'
                    f'{content}\n'
                    f'{quantity}шт\n'
                    f'{price}грн',
        )
