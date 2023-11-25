from os import getenv

from pymongo import MongoClient
from pymongo.database import Database

from support_bot.misc import (
    MONGO_DB_NAME,
    MONGO_HOST,
    MONGO_PASSWORD,
    MONGO_PORT,
    MONGO_USER_NAME,
)


def get_mongo_db() -> Database:
    uri = f"mongodb://{MONGO_USER_NAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB_NAME}"
    client = MongoClient(uri, authSource="admin")
    db: Database = client[MONGO_DB_NAME]
    return db
