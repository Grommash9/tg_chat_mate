from support_bot.db.client import get_mongo_db
from support_bot.db.collection_names import FILES_COLLECTION


def new_file(file_data):
    db = get_mongo_db()
    collection = db[FILES_COLLECTION]
    collection.insert_one(file_data).inserted_id


def get_file(uuid):
    db = get_mongo_db()
    collection = db[FILES_COLLECTION]
    file_document = collection.find_one({"_id": uuid})
    return file_document


def find_file_by_hash(hash):
    db = get_mongo_db()
    collection = db[FILES_COLLECTION]
    file_document = collection.find_one({"hash": hash})
    return file_document
