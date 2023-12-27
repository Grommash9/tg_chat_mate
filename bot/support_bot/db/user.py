from aiogram.types import User
from pymongo.errors import DuplicateKeyError

from support_bot.db.client import get_mongo_db, get_async_mongo_db
from support_bot.db.collection_names import USER_COLLECTION_NAME


async def new_user(user: User):
    db = await get_async_mongo_db()
    collection = db[USER_COLLECTION_NAME]
    post = {"_id": user.id, "username": user.username, "name": user.full_name}
    try:
        await collection.insert_one(post)
    except DuplicateKeyError:
        pass


def add_photo(user: User, photo_uuid):
    db = get_mongo_db()
    collection = db[USER_COLLECTION_NAME]

    collection.update_one(
        {"_id": user.id}, {"$set": {"photo_uuid": photo_uuid}}
    )


def get_all_users():
    db = get_mongo_db()
    collection = db[USER_COLLECTION_NAME]
    return list(collection.find())
