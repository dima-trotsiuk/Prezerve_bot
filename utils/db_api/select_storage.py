from .models import engine, storage


def select_storage_func():

    conn = engine.connect()
    products = storage.select()
    products = conn.execute(products)
    products = products.fetchall()
    conn.close()

    return products
