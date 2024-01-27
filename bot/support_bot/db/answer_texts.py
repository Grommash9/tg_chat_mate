from support_bot.db.client import get_async_mongo_db
from support_bot.db.collection_names import TEXTS_COLLECTION


async def start_text(language_code: str) -> str:
    db = await get_async_mongo_db()
    collection = db[TEXTS_COLLECTION]
    text = await collection.find_one(
        {"type": "start_text", "language_code": language_code}
    )
    return text.get("text")
