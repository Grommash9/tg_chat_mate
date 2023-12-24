# Small script to generate random messages for existing users for testing feel free to remove it later
import json
from random import randint, choice
from datetime import datetime, timedelta
from copy import deepcopy
import random
from bson.objectid import ObjectId


attachment = [
    {
        "file_id": "7a6e101f-e3b7-473e-b4c4-65cf9401c7b7",
        "mime_type": "image/jpeg",
        "file_name": None,
    },
    {
        "file_id": "2ad01180-7ede-4ecc-b709-f7184c1a51ab",
        "mime_type": "image/jpeg",
        "file_name": None,
    },
    {
        "file_id": "48e9b5f6-065f-4d37-8e18-4c127487551c",
        "mime_type": "audio/ogg",
        "file_name": None,
    },
    {
        "file_id": "280721f9-b907-4025-95c1-18b3fc4747c5",
        "mime_type": "video/webm",
        "file_name": None,
    },
    {
        "file_id": "efdc741f-1b23-4778-bcf1-3f0f64dfc2c9",
        "mime_type": "image/webp",
        "file_name": None,
    },
    {
        "file_id": "9e40520a-5526-4eee-8dcb-47e1bd333235",
        "mime_type": "video/mp4",
        "file_name": None,
    },
    {"latitude": 51.479224, "longitude": -0.157111},
    {
        "file_id": "18a6ceef-c61b-4007-8cb1-b29459acd7c6",
        "mime_type": "image/jpeg",
        "file_name": "IMG_5968.JPG",
    },
    {
        "file_id": "7b9df559-7475-4fa3-96fc-bffc1cbf8c1e",
        "mime_type": "application/x-rar",
        "file_name": "bot+(3).rar",
    },
]


users = [
    {"_id": 859203, "name": "Ethan Taylor"},
    {"_id": 473910, "name": "Olivia Brown"},
    {"_id": 721058, "name": "Sophia Johnson"},
    {"_id": 537920, "name": "Liam Wilson"},
    {"_id": 684302, "name": "Ava Martinez"},
    {"_id": 893710, "name": "Isabella Davis"},
    {"_id": 321087, "name": "Mason Rodriguez"},
    {"_id": 560394, "name": "Mia Anderson"},
    {"_id": 792468, "name": "Noah Thomas"},
    {"_id": 438201, "name": "Emily Jackson"},
    {"_id": 615093, "name": "Charlotte Garcia"},
    {"_id": 507182, "name": "Jacob Lee"},
    {"_id": 824609, "name": "Amelia Hernandez"},
    {"_id": 398512, "name": "Michael Smith"},
    {"_id": 719530, "name": "Harper Martinez"},
    {"_id": 352489, "name": "Evelyn Jones"},
]


user_messages = [
    "Hello, I have a question about my account.",
    "Can you help me with a billing issue?",
    "I'm experiencing a problem with the app.",
    "Hi, I'd like to update my contact information.",
    "Good morning, I need assistance with my subscription.",
]

manager_messages = [
    "Certainly, I can help you with that. What seems to be the problem?",
    "I'm here to help. Could you please provide me with more details?",
    "Of course, I'd be happy to assist. Please tell me more about the issue.",
    "Hello! I'd be glad to help you with your request. What do you need to update?",
    "Good morning! I'm here to assist you. What can I do for you today?",
]


base_message = {
    "_id": {"$oid": ""},
    "message_id": 0,
    "chat_id": {"$numberLong": ""},
    "message_text": "",
    "date": {"$date": ""},
    "from_user": {"$numberLong": ""},
    "reply_to_message": {"$oid": ""}
}


def random_date():
    return datetime.now() - timedelta(days=randint(0, 30))


messages = []
message_id = 500

for user in users:
    manager_answer_id, user_message_id = None, None
    for _ in range(0, 100):
        user_message_id = str(ObjectId())
        user_msg = deepcopy(base_message)
        user_msg["_id"]["$oid"] = user_message_id
        user_msg["message_id"] = message_id
        user_msg["chat_id"]["$numberLong"] = str(user["_id"])
        user_msg["message_text"] = choice(user_messages)
        user_msg["date"]["$date"] = random_date().strftime(
            "%Y-%m-%dT%H:%M:%S.000Z"
        )
        user_msg["from_user"]["$numberLong"] = str(user["_id"])
        if random.randint(0, 10) == 10:
            user_msg["attachment"] = random.choice(attachment)
        if manager_answer_id is not None and random.randint(0, 7) == 5:
            user_msg["reply_to_message"]["$oid"] = manager_answer_id
        else:
            user_msg.pop("reply_to_message")
        messages.append(user_msg)
        message_id += 1

        manager_answer_id = str(ObjectId())
        manager_msg = deepcopy(base_message)
        manager_msg["_id"]["$oid"] = manager_answer_id
        manager_msg["message_id"] = message_id
        manager_msg["chat_id"]["$numberLong"] = str(user["_id"])
        manager_msg["message_text"] = choice(manager_messages)
        if user_message_id is not None and random.randint(0, 10) == 5:
            manager_msg["reply_to_message"]["$oid"] = user_message_id
        else:
            manager_msg.pop("reply_to_message")
        manager_msg["date"]["$date"] = (
            random_date() + timedelta(minutes=5)
        ).strftime(
            "%Y-%m-%dT%H:%M:%S.000Z"
        )
        manager_msg["from_user"]["$numberLong"] = str(6769482228)
        manager_msg["manager_name"] = "Root admin"
        if random.randint(0, 10) == 10:
            manager_msg["attachment"] = random.choice(attachment)
        messages.append(manager_msg)
        message_id += 1


file_path = "generated_messages.json"
with open(file_path, "w") as file:
    json.dump(messages, file)
