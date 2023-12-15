from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from support_bot import db
from support_bot.misc import (
    router,
    send_update_to_socket,
    upload_file_to_db_using_file_id,
)


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    if message.chat.type != "private":
        return
    assert message.from_user is not None
    db.user.new_user(message.from_user)
    message_document = db.message.new_message(message, unread=True)
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")

    try:
        await send_update_to_socket(message_document)
    except Exception as e:
        await message.answer(f"Manager delivery error! {str(e)}")

    try:
        profile_photos = await message.from_user.get_profile_photos(0, 1)
        photo_file_db_uuid = await upload_file_to_db_using_file_id(profile_photos.photos[-1][-1].file_id)
        db.user.add_photo(message.from_user, photo_file_db_uuid["file_id"])
    except Exception as e:
        print(f"Error on getting photo for user {message.from_user.id}: {str(e)}")
