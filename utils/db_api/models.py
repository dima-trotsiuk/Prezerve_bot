from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, DateTime, \
    ForeignKey, UnicodeText, Enum
from datetime import datetime

from data.config import database

engine = create_engine(
    f"{database['type']}+pymysql://"
    f"{database['username']}:"
    f"{database['password']}@"
    f"{database['host']}/"
    f"{database['database_name']}?charset=utf8mb4")

metadata = MetaData()

Users = Table('Users', metadata,
              Column('telegram_id', String(255), nullable=False, unique=True),
              Column('first_name', String(255), nullable=False),
              Column('username', String(255)),
              Column('created_on', DateTime(), default=datetime.now),
              Column('number', String(255))
              )
Categories = Table('Categories', metadata,
                   Column('id', Integer(), primary_key=True),
                   Column('title', String(255), nullable=False),  # nullable=False =NOT NULL
                   )
Storage = Table('Storage', metadata,
                Column('id', Integer(), primary_key=True),
                Column('title', String(255), nullable=False),  # nullable=False =NOT NULL
                Column('content', UnicodeText(collation='utf8mb4_unicode_ci'), nullable=False),
                Column('quantity', Integer(), default=0),
                Column('category_id', Integer(), ForeignKey('Categories.id')),
                Column('price', Integer(), default=0),
                Column('photo_id', String(255)),
                )

Orders = Table('Orders', metadata,
               Column('id', Integer(), primary_key=True),
               Column('price', Integer()),
               Column('platform', Enum('instagram', 'telegram'), default='telegram'),
               Column('ttn', String(255)),
               Column('status', Enum('processing', 'completed'), default='processing'),
               Column('date', DateTime(), default=datetime.now),
               Column('user_telegram_id', String(255), ForeignKey('Users.telegram_id'))
               )

Order_products = Table('Order_products', metadata,
                       Column('id', Integer(), primary_key=True),
                       Column('category_id', Integer(), ForeignKey('Categories.id')),
                       Column('product_id', Integer(), ForeignKey('Storage.id')),
                       Column('order_id', Integer(), ForeignKey('Orders.id')),
                       Column('quantity', Integer()),
                       Column('user_telegram_id', String(255), ForeignKey('Users.telegram_id'))
                       )


# metadata.create_all(engine)   створення таблиці
