from pymongo import MongoClient
from pymongo.database import Database
from os import getenv

MONGO_USER_NAME = getenv("MONGO_INITDB_ROOT_USERNAME")
MONGO_PASSWORD = getenv("MONGO_INITDB_ROOT_PASSWORD")
MONGO_HOST = getenv("MONGO_HOST", getenv('SERVER_IP_ADDRESS'))
MONGO_PORT = getenv("MONGO_PORT", 27017)
MONGO_DB_NAME = getenv("MONGO_INITDB_DATABASE", "bot_support_db")


def get_mongo_db() -> Database:
    uri = f"mongodb://{MONGO_USER_NAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB_NAME}"
    client = MongoClient(uri, authSource="admin")
    db: Database = client[MONGO_DB_NAME]
    return db
