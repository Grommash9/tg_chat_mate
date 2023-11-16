from aiogram.types import Message
from db.client import get_mongo_db
from pymongo.errors import DuplicateKeyError

USER_COLLECTION_NAME = 'message'

def new_message(message: Message):
    db = get_mongo_db()
    collection = db[USER_COLLECTION_NAME]
    post = {"message_id": message.message_id, "chat_id": message.chat.id, "message_text": message.text, "date": message.date, "from_user": message.from_user.id}
    collection.insert_one(post).inserted_id


def get_all_chat_messages(chat_id):
    db = get_mongo_db()
    collection = db[USER_COLLECTION_NAME]
    return [data for data in collection.find(chat_id=chat_id)]
