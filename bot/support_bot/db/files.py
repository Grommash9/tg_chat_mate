from support_bot.db.client import get_async_mongo_db
from support_bot.db.collection_names import FILES_COLLECTION


async def new_file(file_data):
    db = await get_async_mongo_db()
    collection = db[FILES_COLLECTION]
    await collection.insert_one(file_data)


async def get_file(uuid):
    db = await get_async_mongo_db()
    collection = db[FILES_COLLECTION]
    file_document = await collection.find_one({"_id": uuid})
    return file_document


async def find_file_by_hash(file_hash):
    db = await get_async_mongo_db()
    collection = db[FILES_COLLECTION]
    file_document = await collection.find_one({"hash": file_hash})
    return file_document
