from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, DateTime, \
    ForeignKey, LargeBinary
from sqlalchemy.sql import select, and_
from datetime import datetime

from data.config import database

engine = create_engine(
    f"{database['type']}+pymysql://{database['username']}:{database['password']}@{database['host']}/{database['database_name']}")

metadata = MetaData()

users = Table('users', metadata,
              Column('first_name', String(255), nullable=False),
              Column('username', String(255)),
              Column('id', Integer, nullable=False, unique=True),
              Column('created_on', DateTime(), default=datetime.now)
              )

storage = Table('storage', metadata,
                Column('id', Integer(), primary_key=True),
                Column('title', String(200), nullable=False),  # nullable=False =NOT NULL
                Column('photo', LargeBinary),
                Column('content', Text(), nullable=False),
                Column('quantity', Integer(), default=0),
                )

metadata.create_all(engine)  # створення таблиці
