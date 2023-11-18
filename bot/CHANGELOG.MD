# 0.0.1 Unreleased
    - Bot file system refactoring
    - New bot routes
        - `/tg-bot/chat-list` GET getting chat list (unread count, last message text, last message date)
        - `/tg-bot/get-messages/{chat_id}` GET for get all messages by tg chat id
        - `/tg-bot/mark-as-read` POST for mark message as read from UI
        - `/tg-bot/new-message` POST for send message from UI into bot