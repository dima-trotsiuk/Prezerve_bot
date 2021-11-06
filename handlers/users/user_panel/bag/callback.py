from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from handlers.users.user_panel.bag.checkout import validation
from handlers.users.user_panel.bag.edit import show_buttons_edit_bag
from handlers.users.user_panel.bag.is_empty_bag import is_empty_bag_func
from handlers.users.user_panel.bag.show_text_and_buttons import show_text_and_buttons
from keyboards.inline.user.bag.callback_datas import show_buttons_callback
from handlers.users.user_panel.bag.clear import clear_bag
from loader import dp


@dp.message_handler(text="Корзина 🛒")
async def get_storage_func(message: types.Message):
    if await is_empty_bag_func(message):
        await show_text_and_buttons(message)


@dp.callback_query_handler(show_buttons_callback.filter(type_command="show_buttons_bag"))
async def command_processing_catalog(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=1)

    if await is_empty_bag_func(call.message):
        command = callback_data.get("command")

        if command == "edit":
            await show_buttons_edit_bag(call.message)
        elif command == "clear":
            await clear_bag(call.message)
        elif command == "promo_code":
            await call.message.answer(f"В разработке.")
        elif command == "checkout":
            await validation(call.message)
