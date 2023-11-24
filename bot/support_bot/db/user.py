from aiogram.types import User
from pymongo.errors import DuplicateKeyError
from support_bot.db.client import get_mongo_db
from support_bot.db.collection_names import USER_COLLECTION_NAME


def new_user(user: User):
    db = get_mongo_db()
    collection = db[USER_COLLECTION_NAME]
    post = {"_id": user.id, "username": user.username, "name": user.full_name}
    try:
        collection.insert_one(post).inserted_id
    except DuplicateKeyError:
        pass


def get_all_users():
    db = get_mongo_db()
    collection = db[USER_COLLECTION_NAME]
    return [data for data in collection.find()]
