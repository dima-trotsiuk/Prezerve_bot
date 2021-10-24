from aiogram.utils.callback_data import CallbackData

edit_storage_callback = CallbackData("edit_storage", "id", "type_command")
new_product_select_category_callback = CallbackData("new_product_select", "category_id", "type_command")
product_info_for_id_callback = CallbackData("product_info_for_id", "command", "product_id", "type_command")
