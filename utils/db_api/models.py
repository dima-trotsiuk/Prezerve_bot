from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, DateTime, \
    ForeignKey, LargeBinary, Float, UnicodeText
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
              Column('first_name', String(255), nullable=False),
              Column('username', String(255)),
              Column('id', Integer, nullable=False, unique=True),
              Column('created_on', DateTime(), default=datetime.now)
              )

storage = Table('storage', metadata,
                Column('id', Integer(), primary_key=True),
                Column('title', String(255), nullable=False),  # nullable=False =NOT NULL
                Column('content', UnicodeText(collation='utf8mb4_unicode_ci'), nullable=False),
                Column('quantity', Integer(), default=0),
                Column('category_id', Integer(), ForeignKey('categories.id')),
                Column('price', Float(), default=0.0),
                Column('photo_id', String(255)),
                )

categories = Table('categories', metadata,
                   Column('id', Integer(), primary_key=True),
                   Column('title', String(255), nullable=False),  # nullable=False =NOT NULL
                   )


metadata.create_all(engine)  # створення таблиці
