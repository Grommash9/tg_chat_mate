import re
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import config
import db_api
import ast
import json

bot = Bot(token=config.telegram_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'Welcome to the bot')


@dp.message_handler()
async def any_message_answer(message: types.Message):
    if message.from_user.id in config.managers_id:
        if message.reply_to_message:
            try:
                parsing_target = '[(]{1}(.{0,20})[)]{1}'
                reply_id = re.findall(parsing_target, str(message.reply_to_message.text))
                username_parsing = '([@]{1}.{0,30})[ (]{2}'
                username = re.findall(username_parsing, str(message.reply_to_message.text))
                await bot.send_message(chat_id=reply_id[0],
                                       text='Reply from manager: \n\n'
                                            f'{message.text}')
                try:
                    await bot.send_message(chat_id=message.from_user.id,
                                           text=f'Your reply for {username[0]} has been successfully delivered')
                    message_set = False
                    reply_message_id = message.reply_to_message.message_id
                    message_list = db_api.get_all_messages()
                    for message_data in message_list:
                        local_message_list = ast.literal_eval(message_data[1])
                        for local_messages in local_message_list:
                            if local_messages['message_id'] == reply_message_id:
                                messages_set_id = message_data[0]
                                message_set = True
                    if message_set:
                        old_message_data = db_api.get_singe_message(id=messages_set_id)
                        local_old_message_list = ast.literal_eval(old_message_data[1])
                        old_text = old_message_data[2]
                        for old_local_messages in local_old_message_list:
                            await bot.edit_message_text(chat_id=old_local_messages['chat_id'], message_id=old_local_messages['message_id'], text=f"{old_text}\n\n✓")
                        db_api.delete_message(id=messages_set_id)

                except IndexError:
                    await bot.send_message(chat_id=message.from_user.id,
                                           text=f'Your reply for {reply_id[0]} has been successfully delivered')
            except IndexError:
                await bot.send_message(chat_id=message.from_user.id,
                                       text=f"Can't find user id or username in this message")
        else:
            await bot.send_message(chat_id=message.from_user.id,
                                   text='You can only reply to messages')
    else:
        current_messages_list = []
        for managers in config.managers_id:
            text_to_send = f"Message from @{message.from_user.username} ({message.from_user.id}):\n\n{message.text}"
            message_data = (await bot.send_message(chat_id=managers,
                                   text=text_to_send))
            current_messages_list.append({
                'message_id': message_data['message_id'],
                'chat_id': message_data['chat']['id']
            })
        db_api.add_message(message_data=str(current_messages_list), text=text_to_send)
        await bot.send_message(chat_id=message.from_user.id,
                               text='Your message has been successfully delivered to the manager')


if __name__ == '__main__':
    executor.start_polling(dp)

