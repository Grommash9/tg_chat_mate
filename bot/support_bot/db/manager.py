import bcrypt
from pymongo.errors import DuplicateKeyError

from support_bot.db.client import get_mongo_db
from support_bot.db.collection_names import MANAGER_COLLECTION_NAME


def hash_password(password: str):
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed


def get_manager_by_username(username):
    db = get_mongo_db()
    collection = db[MANAGER_COLLECTION_NAME]
    manager = collection.find_one({"username": username})
    return manager


def new_manager(full_name, username, password, root=False):
    db = get_mongo_db()
    collection = db[MANAGER_COLLECTION_NAME]

    print("manager founded", collection.find_one({"username": username}))

    if collection.find_one({"username": username}):
        raise DuplicateKeyError("Username is not unique")

    manager = {
        "username": username,
        "hashed_password": hash_password(password).decode("utf-8"),
        "full_name": full_name,
        "tokens": [],
    }
    if root:
        manager["root"] = True
    collection.insert_one(manager)


def check_password(username: str, password: str) -> bool:
    db = get_mongo_db()
    collection = db[MANAGER_COLLECTION_NAME]
    manager = collection.find_one({"username": username})
    if not manager:
        return False
    hashed_password = manager["hashed_password"].encode("utf-8")
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
