from aiogram.types import User
from pymongo.errors import DuplicateKeyError

from support_bot.db.client import get_async_mongo_db, get_mongo_db
from support_bot.db.collection_names import USER_COLLECTION_NAME
from support_bot.misc import save_user_photo


async def new_user(user: User):
    db = await get_async_mongo_db()
    collection = db[USER_COLLECTION_NAME]
    post = {"_id": user.id, "username": user.username, "name": user.full_name}
    try:
        await collection.insert_one(post)
        await save_user_photo(user)
    except DuplicateKeyError:
        pass


async def add_photo(user: User, photo_uuid):
    db = await get_async_mongo_db()
    collection = db[USER_COLLECTION_NAME]
    await collection.update_one(
        {"_id": user.id}, {"$set": {"photo_uuid": photo_uuid}}
    )


async def update(user_id: int, info: dict):
    db = await get_async_mongo_db()
    collection = db[USER_COLLECTION_NAME]
    find_user = await collection.find_one({"_id": user_id})
    if not find_user:
        return False
    for key, value in info.items():
        await collection.update_one({"_id": user_id}, {"$set": {key: value}})
    return True


def get_all_users():
    db = get_mongo_db()
    collection = db[USER_COLLECTION_NAME]
    return list(collection.find())


async def get_user(user_id: int):
    db = await get_async_mongo_db()
    collection = db[USER_COLLECTION_NAME]
    info = await collection.find_one({"_id": user_id})
    if not info:
        return None
    return info
