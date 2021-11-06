from aiogram.utils.callback_data import CallbackData

show_buttons_callback = CallbackData("show_buttons", "command", "type_command")
edit_products_in_bag_callback = CallbackData("edit_products_in_bag", "command", "index_product", "type_command")
message_to_admin_callback = CallbackData("message_to_admin", "order_id", "type_command")
