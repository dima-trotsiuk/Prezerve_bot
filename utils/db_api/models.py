from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, DateTime, \
    ForeignKey, LargeBinary, Float, UnicodeText, Enum
from sqlalchemy.sql import select, and_
from datetime import datetime

from data.config import database

engine = create_engine(
    f"{database['type']}+pymysql://"
    f"{database['username']}:"
    f"{database['password']}@"
    f"{database['host']}/"
    f"{database['database_name']}?charset=utf8mb4")

metadata = MetaData()

users = Table('users', metadata,
              Column('telegram_id', String(255), nullable=False, unique=True),
              Column('first_name', String(255), nullable=False),
              Column('username', String(255)),
              Column('created_on', DateTime(), default=datetime.now)
              )
categories = Table('categories', metadata,
                   Column('id', Integer(), primary_key=True),
                   Column('title', String(255), nullable=False),  # nullable=False =NOT NULL
                   )
storage = Table('storage', metadata,
                Column('id', Integer(), primary_key=True),
                Column('title', String(255), nullable=False),  # nullable=False =NOT NULL
                Column('content', UnicodeText(collation='utf8mb4_unicode_ci'), nullable=False),
                Column('quantity', Integer(), default=0),
                Column('category_id', Integer(), ForeignKey('categories.id')),
                Column('price', Integer(), default=0),
                Column('photo_id', String(255)),
                )

orders = Table('orders', metadata,
               Column('id', Integer(), primary_key=True),
               Column('price', Integer()),
               Column('platform', Enum('instagram', 'telegram'), default='telegram'),
               Column('ttn', String(255)),
               Column('status', Enum('processing', 'completed'), default='processing'),
               Column('date', DateTime(), default=datetime.now),
               Column('user_telegram_id', String(255), ForeignKey('users.telegram_id'))
               )

order_products = Table('order_products', metadata,
                       Column('id', Integer(), primary_key=True),
                       Column('category_id', Integer(), ForeignKey('categories.id')),
                       Column('product_id', Integer(), ForeignKey('storage.id')),
                       Column('order_id', Integer(), ForeignKey('orders.id')),
                       Column('quantity', Integer()),
                       )
metadata.create_all(engine)  # створення таблиці
