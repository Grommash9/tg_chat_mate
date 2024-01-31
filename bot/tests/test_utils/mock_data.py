"""
Data for mocking.
"""

# Database documents mock
VALID_USER_DOCUMENT = {
    "is_bot": True,
    "first_name": "John",
    "last_name": "Due",
    "username": "johndue",
    "language_code": "eng",
    "is_premium": True,
    "added_to_attachment_menu": True,
    "can_join_groups": True,
    "can_read_all_group_messages": True,
    "supports_inline_queries": True,
}

# Mock for successful responses
NOTIFICATION_SUCCCESS = {"result": "notification sent successfully"}

USER_INFO_UPDATE_SUCCESS = {"result": "User info updated"}

# Mock for error responses
INVALID_USER_ID_IN_URL = {
    "result": "user_id param error: invalid literal for int() with base 10: "
    "'test_user_id'"
}

MANAGER_ACTION_WRONG_ACTION = {
    "result": "user_id or action param error: Wrong action"
}

FLOOD_CHECK_ERROR = {"result": "notification don`t pass flood check"}

NOTIFICATION_FAILED = {"result": "cant send notification to user, error test"}

USER_NOT_FOUND_ERROR = {"result": "User not found"}
