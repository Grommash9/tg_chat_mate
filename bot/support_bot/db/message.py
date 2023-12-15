from aiogram.types import Message
from pymongo import DESCENDING

from support_bot.db.client import get_mongo_db
from support_bot.db.collection_names import (
    MESSAGE_COLLECTION_NAME,
    USER_COLLECTION_NAME,
)


def new_message(
    message: Message,
    unread=False,
    attachment: dict | None = None,
    location: dict | None = None,
    manager_name: str | None = None,
):
    db = get_mongo_db()
    collection = db[MESSAGE_COLLECTION_NAME]
    post = {
        "message_id": message.message_id,
        "chat_id": message.chat.id,
        "message_text": message.text if message.text is not None else message.caption,
        "date": message.date,
        "from_user": message.from_user.id,  # type: ignore[union-attr]
    }
    if unread:
        post["unread"] = unread
    if attachment:
        post["attachment"] = attachment
    if location:
        post["location"] = location
    if manager_name:
        post["manager_name"] = manager_name
    collection.insert_one(post).inserted_id
    return post


def convert_objects_str(data):
    for json_bad_fields in ["_id", "date"]:
        if json_bad_fields in data:
            data[json_bad_fields] = str(data[json_bad_fields])
    return data


def mark_as_read(chat_id, message_id):
    db = get_mongo_db()
    collection = db[MESSAGE_COLLECTION_NAME]
    filter_condition = {"message_id": int(message_id), "chat_id": int(chat_id)}
    update_result = collection.update_one(filter_condition, {"$unset": {"unread": ""}})
    return update_result.modified_count


def mark_chat_as_read(chat_id):
    db = get_mongo_db()
    collection = db[MESSAGE_COLLECTION_NAME]
    filter_condition = {"chat_id": int(chat_id)}
    update_result = collection.update_many(filter_condition, {"$unset": {"unread": ""}})
    return update_result.modified_count


def get_all_chat_messages(chat_id):
    db = get_mongo_db()
    collection = db[MESSAGE_COLLECTION_NAME]
    filter_dict = {"chat_id": chat_id}
    return [convert_objects_str(data) for data in collection.find(filter_dict)]


def get_chat_list():
    db = get_mongo_db()
    messages_collection = db[MESSAGE_COLLECTION_NAME]
    pipeline = [
        # Sort by user and date first to prepare for the grouping
        {"$sort": {"chat_id": 1, "date": DESCENDING}},
        # Group by user ID to get the last message and its time
        {
            "$group": {
                "_id": "$chat_id",
                "last_message_text": {"$first": "$message_text"},
                "last_message_time": {"$first": "$date"},
                # Add all messages to an array to calculate unread count later
                "messages": {"$push": {"unread": "$unread", "message_text": "$message_text"}},
            }
        },
        # Add a field to count unread messages
        {
            "$addFields": {
                "unread_count": {
                    "$size": {
                        "$filter": {
                            "input": "$messages",
                            "as": "message",
                            "cond": {"$eq": ["$$message.unread", True]},
                        }
                    }
                }
            }
        },
        # Project the desired fields
        {
            "$project": {
                "user_id": "$_id",
                "last_message_text": 1,
                "photo_uuid": 1,
                "unread_count": 1,
                "last_message_time": {
                    # Convert the datetime to string
                    "$dateToString": {
                        "format": "%Y-%m-%d %H:%M:%S",
                        "date": "$last_message_time",
                    }
                },
            }
        },
        # Lookup to join with user details
        {
            "$lookup": {
                "from": USER_COLLECTION_NAME,
                "localField": "user_id",
                "foreignField": "_id",
                "as": "user_details",
            }
        },
        # Unwind the result of the lookup because lookup returns an array
        {"$unwind": "$user_details"},
        # Add fields for user details
        {
            "$addFields": {
                "username": "$user_details.username",
                "name": "$user_details.name",
                "photo_uuid": "$user_details.photo_uuid",
            }
        },
        # Sort by the last message time in descending order
        {"$sort": {"last_message_time": DESCENDING}},
        # Project to adjust the final output
        {
            "$project": {
                "user_id": 1,
                "last_message_text": 1,
                "unread_count": 1,
                "last_message_time": 1,
                "photo_uuid": 1,
                "username": 1,
                "name": 1,
                "_id": 0,  # Exclude the _id field from the final output
            }
        },
    ]

    # Execute the aggregation pipeline
    results = list(messages_collection.aggregate(pipeline))  # type: ignore[arg-type]
    return results
