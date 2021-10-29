from aiogram.utils.callback_data import CallbackData

order_management_callback = CallbackData("order_management", "command", "type_command")
add_product_to_order_callback = CallbackData("product_info_for_id", "command", "product_id", "quantity_selected", "type_command")

