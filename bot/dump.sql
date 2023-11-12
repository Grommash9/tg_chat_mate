CREATE TABLE IF NOT EXISTS tg_user (
    tg_chat_id BIGINT PRIMARY KEY,
    full_name TEXT,
    user_name TEXT,
    locale TEXT
);
