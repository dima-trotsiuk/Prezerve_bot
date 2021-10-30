from .models import engine, Storage


def select_storage_func(category):
    conn = engine.connect()
    if category == 0:
        products = Storage.select()
    else:
        products = Storage.select().where(Storage.c.category_id == category)
    products = conn.execute(products)
    products = products.fetchall()
    conn.close()

    return products
