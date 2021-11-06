from utils.db_api.models import engine, Storage


async def get_poducts_for_cat_func(category_id):
    conn = engine.connect()
    products_info = Storage.select().where(Storage.c.category_id == category_id)
    products_info = conn.execute(products_info)
    products_info = products_info.fetchall()

    conn.close()
    return products_info
