import datetime

import bcrypt
import jwt
from pymongo.errors import DuplicateKeyError

from support_bot.db.client import get_mongo_db
from support_bot.db.collection_names import MANAGER_COLLECTION_NAME
from support_bot.misc import LONG_GOOD_SECRET_KEY


def hash_password(password: str):
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed


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
    collection.insert_one(manager).inserted_id


def check_password(username: str, password: str) -> bool:
    db = get_mongo_db()
    collection = db[MANAGER_COLLECTION_NAME]
    manager = collection.find_one({"username": username})
    if not manager:
        return False
    hashed_password = manager["hashed_password"].encode("utf-8")
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)


def create_token_for_manager(username: str, days=7) -> str | None:
    db = get_mongo_db()
    collection = db[MANAGER_COLLECTION_NAME]
    manager = collection.find_one({"username": username})
    if not manager:
        return None

    expiration_date = datetime.datetime.utcnow() + datetime.timedelta(days=days)
    token = jwt.encode(
        {"username": username, "exp": expiration_date},
        LONG_GOOD_SECRET_KEY,
        algorithm="HS256",
    )

    # Save the token in the manager's tokens array
    collection.update_one(
        {"_id": manager["_id"]},
        {"$push": {"tokens": {"token": token, "expiration_date": expiration_date}}},
    )
    return token


def get_manager_by_token(token: str | None):
    if token is None:
        return token
    db = get_mongo_db()
    collection = db[MANAGER_COLLECTION_NAME]
    try:
        payload = jwt.decode(
            token,
            LONG_GOOD_SECRET_KEY,
            algorithms=["HS256"],
            options={"verify_signature": False},
        )
        username = payload["username"]
    except jwt.DecodeError:
        return None  # Invalid token

    # Retrieve the manager from the collection
    manager = collection.find_one({"username": username})
    if not manager:
        return None  # Manager not found

    # Check if the token is in the manager's tokens array and not expired
    current_time = datetime.datetime.utcnow()
    for manager_token in manager.get("tokens", []):
        if manager_token["token"] == token and manager_token["expiration_date"] > current_time:
            return manager  # Token is valid and not expired

    return None  # Token is not valid or is expired
