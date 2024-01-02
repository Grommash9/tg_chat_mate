from aiogram import F, types

from support_bot import db
from support_bot.misc import (
    ChatTypeFilter,
    router,
    send_update_to_socket,
    upload_file_to_db_using_file_id,
)


@router.message(ChatTypeFilter(chat_type=["private"]), F.video)
async def video_message_from_user(message: types.Message) -> None:
    if message.video is None:
        return

    attachment = await upload_file_to_db_using_file_id(message.video.file_id)
    message_document = await db.message.new_message(
        message, unread=True, attachment=attachment
    )
    try:
        await send_update_to_socket(message_document)
    except Exception as e:
        await message.answer(f"Manager delivery error! {str(e)}")


@router.message(ChatTypeFilter(chat_type=["private"]), F.video_note)
async def video_note_message_from_user(message: types.Message) -> None:
    if message.video_note is None:
        return

    attachment = await upload_file_to_db_using_file_id(
        message.video_note.file_id
    )
    message_document = await db.message.new_message(
        message, unread=True, attachment=attachment
    )
    try:
        await send_update_to_socket(message_document)
    except Exception as e:
        await message.answer(f"Manager delivery error! {str(e)}")


@router.message(ChatTypeFilter(chat_type=["private"]), F.animation)
async def animation_message_from_user(message: types.Message) -> None:
    if message.animation is None:
        return

    attachment = await upload_file_to_db_using_file_id(
        message.animation.file_id
    )
    message_document = await db.message.new_message(
        message, unread=True, attachment=attachment
    )
    try:
        await send_update_to_socket(message_document)
    except Exception as e:
        await message.answer(f"Manager delivery error! {str(e)}")


@router.message(ChatTypeFilter(chat_type=["private"]), F.location)
async def location_message_from_user(message: types.Message) -> None:
    if message.location is None:
        return

    message_document = await db.message.new_message(
        message,
        unread=True,
        location={
            "latitude": message.location.latitude,
            "longitude": message.location.longitude,
        },
    )
    try:
        await send_update_to_socket(message_document)
    except Exception as e:
        await message.answer(f"Manager delivery error! {str(e)}")


@router.message(ChatTypeFilter(chat_type=["private"]), F.voice)
async def voice_message_from_user(message: types.Message) -> None:
    if message.voice is None:
        return

    attachment = await upload_file_to_db_using_file_id(message.voice.file_id)
    message_document = await db.message.new_message(
        message, unread=True, attachment=attachment
    )
    try:
        await send_update_to_socket(message_document)
    except Exception as e:
        await message.answer(f"Manager delivery error! {str(e)}")


@router.message(ChatTypeFilter(chat_type=["private"]), F.sticker)
async def sticker_message_from_user(message: types.Message) -> None:
    if message.sticker is None:
        return

    attachment = await upload_file_to_db_using_file_id(message.sticker.file_id)
    message_document = await db.message.new_message(
        message, unread=True, attachment=attachment
    )
    try:
        await send_update_to_socket(message_document)
    except Exception as e:
        await message.answer(f"Manager delivery error! {str(e)}")


@router.message(ChatTypeFilter(chat_type=["private"]), F.document)
async def document_message_from_user(message: types.Message) -> None:
    if message.document is None:
        return

    attachment = await upload_file_to_db_using_file_id(
        message.document.file_id, message.document.file_name
    )
    message_document = await db.message.new_message(
        message, unread=True, attachment=attachment
    )
    try:
        await send_update_to_socket(message_document)
    except Exception as e:
        await message.answer(f"Manager delivery error! {str(e)}")


@router.message(ChatTypeFilter(chat_type=["private"]), F.photo)
async def photo_message_from_user(message: types.Message) -> None:
    if message.photo is None:
        return

    attachment = await upload_file_to_db_using_file_id(
        message.photo[-1].file_id,
    )
    message_document = await db.message.new_message(
        message, unread=True, attachment=attachment
    )
    try:
        await send_update_to_socket(message_document)
    except Exception as e:
        await message.answer(f"Manager delivery error! {str(e)}")


@router.message(ChatTypeFilter(chat_type=["private"]))
async def echo_handler(message: types.Message) -> None:
    message_document = await db.message.new_message(message, unread=True)
    try:
        await send_update_to_socket(message_document)
    except Exception as e:
        await message.answer(f"Manager delivery error! {str(e)}")
