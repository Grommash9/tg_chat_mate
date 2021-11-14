# - *- coding: utf- 8 - *-
import random
import sqlite3
import time
from sqlite3 import IntegrityError
import config

# Путь к БД

####################################################################################################
###################################### ФОРМАТИРОВАНИЕ ЗАПРОСА ######################################
# Форматирование запроса с аргументами
def update_format_with_args(sql, parameters: dict):
    values = ", ".join([
        f"{item} = ?" for item in parameters
    ])
    sql = sql.replace("XXX", values)
    return sql, tuple(parameters.values())


# Форматирование запроса без аргументов
def get_format_args(sql, parameters: dict):
    sql += " AND ".join([
        f"{item} = ?" for item in parameters
    ])
    return sql, tuple(parameters.values())


####################################################################################################
########################################### ЗАПРОСЫ К БД ###########################################
# Добавление данных в таблицы
def add_message(message_data, text):
    with sqlite3.connect(config.path_to_db) as db:
        db.execute("INSERT INTO messages "
                   "(message_data, text) "
                   "VALUES (?, ?)",
                   [message_data, text])
        db.commit()



def delete_message(**kwargs):
    with sqlite3.connect(config.path_to_db) as db:
        sql = "DELETE FROM messages WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        db.execute(sql, parameters)
        db.commit()


# Получение пользователей
def get_all_messages():
    with sqlite3.connect(config.path_to_db) as db:
        sql = "SELECT * FROM messages "
        return db.execute(sql).fetchall()


def get_singe_message(**kwargs):
    with sqlite3.connect(config.path_to_db) as db:
        sql = "SELECT * FROM messages WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        return db.execute(sql, parameters).fetchone()