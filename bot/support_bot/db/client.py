import motor.motor_asyncio
from motor.core import AgnosticClient, AgnosticDatabase
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
    connection_data = f"{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB_NAME}"
    uri = f"mongodb://{MONGO_USER_NAME}:{MONGO_PASSWORD}@{connection_data}"
    client: MongoClient = MongoClient(uri, authSource="admin")
    db: Database = client[MONGO_DB_NAME]
    return db


async def get_async_mongo_db() -> AgnosticDatabase:
    connection_data = f"{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB_NAME}"
    uri = f"mongodb://{MONGO_USER_NAME}:{MONGO_PASSWORD}@{connection_data}"
    client: AgnosticClient = motor.motor_asyncio.AsyncIOMotorClient(
        uri, authSource="admin"
    )
    db = client[MONGO_DB_NAME]
    return db
