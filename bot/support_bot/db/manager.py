from typing import Optional

import bcrypt
from pymongo.errors import DuplicateKeyError

from support_bot.data_types import Manager
from support_bot.db.client import get_async_mongo_db
from support_bot.db.collection_names import MANAGER_COLLECTION_NAME


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode("utf-8")


async def get_manager_by_username(username) -> Optional[Manager]:
    db = await get_async_mongo_db()
    collection = db[MANAGER_COLLECTION_NAME]
    manager = await collection.find_one({"username": username})
    return Manager.from_dict(manager) if manager is not None else None


async def update(username: str, info: dict) -> int:
    db = await get_async_mongo_db()
    collection = db[MANAGER_COLLECTION_NAME]
    result = await collection.update_one(
        {"username": username}, {"$set": info}
    )
    return result.modified_count


async def get_managers() -> list[Manager]:
    db = await get_async_mongo_db()
    collection = db[MANAGER_COLLECTION_NAME]
    cursor = collection.find()
    return [Manager.from_dict(manager) async for manager in cursor]


async def delete_manager_by_username(username) -> None:
    db = await get_async_mongo_db()
    collection = db[MANAGER_COLLECTION_NAME]
    await collection.delete_one({"username": username})


async def new_manager(
    full_name, username, password, root=False, activated=True
) -> None:
    db = await get_async_mongo_db()
    collection = db[MANAGER_COLLECTION_NAME]
    if await collection.find_one({"username": username}):
        raise DuplicateKeyError("Username is not unique")

    manager = {
        "username": username,
        "hashed_password": hash_password(password),
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
