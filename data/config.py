import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
admins = [
    580656744,
]

database = {
    'type': os.getenv("type"),
    'username': os.getenv("username_db"),
    'password': os.getenv("password"),
    'database_name': os.getenv("database_name"),
    'host': os.getenv("host")
}

ip = os.getenv("ip")

aiogram_redis = {
    'host': ip,
}

redis = {
    'address': (ip, 6379),
    'encoding': 'utf8'
}
