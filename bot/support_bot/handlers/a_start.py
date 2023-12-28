from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from support_bot import db
from support_bot.misc import ChatTypeFilter, router, send_update_to_socket


@router.message(ChatTypeFilter(chat_type=["private"]), CommandStart())
async def command_start_handler(message: Message) -> None:
    assert message.from_user is not None
    await db.user.new_user(message.from_user)
    message_document = await db.message.new_message(message, unread=True)
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")

    try:
        await send_update_to_socket(message_document)
    except Exception as e:
        await message.answer(f"Manager delivery error! {str(e)}")
