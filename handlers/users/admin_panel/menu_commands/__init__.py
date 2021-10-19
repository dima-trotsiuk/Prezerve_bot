from .get_storage import dp
from handlers.users.admin_panel.menu_commands.edit_storage.edit_storage import dp
from handlers.users.admin_panel.menu_commands.edit_storage.new_product_states import dp
from .order_management import dp
from .search_for_ttn import dp
from .statistics import dp

__all__ = ["dp"]