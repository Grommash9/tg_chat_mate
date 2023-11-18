from aiogram import types
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from support_bot import db
from support_bot.misc import router


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    db.user.new_user(message.from_user)
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


@router.message()
async def echo_handler(message: types.Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
        db.message.new_message(message, unread=True)
    except TypeError:
        await message.answer("Nice try!")



