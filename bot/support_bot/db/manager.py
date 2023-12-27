import bcrypt
from pymongo.errors import DuplicateKeyError

from support_bot.db.client import get_async_mongo_db
from support_bot.db.collection_names import MANAGER_COLLECTION_NAME


def hash_password(password: str):
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed


async def get_manager_by_username(username):
    db = await get_async_mongo_db()
    collection = db[MANAGER_COLLECTION_NAME]
    manager = await collection.find_one({"username": username})
    return manager


async def new_manager(
    full_name, username, password, root=False, activated=True
):
    db = await get_async_mongo_db()
    collection = db[MANAGER_COLLECTION_NAME]
    if await collection.find_one({"username": username}):
        raise DuplicateKeyError("Username is not unique")

    manager = {
        "username": username,
        "hashed_password": hash_password(password).decode("utf-8"),
        "full_name": full_name,
    }
    if root:
        manager["root"] = True
    if activated:
        manager["activated"] = True
    await collection.insert_one(manager)


async def check_password(username: str, password: str) -> bool:
    db = await get_async_mongo_db()
    collection = db[MANAGER_COLLECTION_NAME]
    manager = await collection.find_one({"username": username})
    if not manager:
        return False
    hashed_password = manager["hashed_password"].encode("utf-8")
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
