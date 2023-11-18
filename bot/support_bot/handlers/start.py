from aiogram import types
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from support_bot import db
from support_bot.misc import router, SERVER_IP_ADDRESS
import aiohttp

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    db.user.new_user(message.from_user)
    db.message.new_message(message, unread=True)
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


@router.message()
async def echo_handler(message: types.Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
        db.message.new_message(message, unread=True)
        try:
            await send_update_to_socket(message.text, message.chat.id)
        except Exception as e:
            await message.answer(f"Manager delivery error! {str(e)}")
    except TypeError:
        await message.answer("Nice try!")


async def send_update_to_socket(text, chat_id):
    async with aiohttp.ClientSession() as session:
        post_data = {'text': text, 'chat_id': chat_id}
        async with session.post(f'https://{SERVER_IP_ADDRESS}/send-message', json=post_data) as resp:
            print(resp.status)
            print(await resp.text())

