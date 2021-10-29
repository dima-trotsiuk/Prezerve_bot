from aiogram.utils.callback_data import CallbackData

select_category_callback = CallbackData("new_product_select", "category_id", "type_command")
select_products_callback = CallbackData("edit_storage", "id", "type_command")