from .models import engine, storage


def select_storage_func(category):
    conn = engine.connect()
    if category == 0:
        products = storage.select()
    else:
        products = storage.select().where(storage.c.category_id == category)
    products = conn.execute(products)
    products = products.fetchall()
    conn.close()

    return products
