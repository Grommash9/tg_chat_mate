import aiohttp
from aiogram import types
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from support_bot import db
from support_bot.misc import router, send_update_to_socket


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    db.user.new_user(message.from_user)
    db.message.new_message(message, unread=True)
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


@router.message()
async def echo_handler(message: types.Message) -> None:
    try:
        db.message.new_message(message, unread=True)
        try:
            await send_update_to_socket(message)
        except Exception as e:
            await message.answer(f"Manager delivery error! {str(e)}")
    except TypeError:
        await message.answer("Nice try!")
