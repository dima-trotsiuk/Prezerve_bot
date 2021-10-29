from handlers.users.admin_panel.menu_commands.get_storage.show_products import dp
from handlers.users.admin_panel.menu_commands.edit_storage.show_buttons import dp
from handlers.users.admin_panel.menu_commands.edit_storage.new_product import dp
from handlers.users.admin_panel.menu_commands.edit_storage.edit_product import dp
from handlers.users.admin_panel.menu_commands.order_management.add_order import dp
from handlers.users.admin_panel.menu_commands.order_management.show_buttons import dp

from .search_for_ttn import dp
from .statistics import dp

__all__ = ["dp"]