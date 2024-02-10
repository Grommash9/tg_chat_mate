from aiogram import F
from aiogram.exceptions import TelegramNotFound
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from support_bot import db, markups
from support_bot.markups.main_menu import LanguageCallback
from support_bot.misc import ChatTypeFilter, router


@router.message(ChatTypeFilter(chat_type=["private"]), CommandStart())
async def command_start_handler(message: Message) -> None:
    assert message.from_user is not None
    await db.user.new_user(message.from_user)
    choose_language_text = await db.user.choose_language(message.chat.id)
    language_info = await db.user.get_all_active_languages()
    if language_info:
        await message.answer(
            text=choose_language_text,
            reply_markup=markups.main_menu.choosing_language(language_info),
        )
        return

    await message.answer(text="Some start text")
    # TODO ADD START MESSAGE
    # try:
    #     await send_update_to_socket(message_document)
    # except Exception as e:
    #     await message.answer(f"Manager delivery error! {str(e)}")


@router.callback_query(LanguageCallback.filter(F.action == "set_language"))
async def set_language(
    call: CallbackQuery, callback_data: LanguageCallback
) -> None:
    await call.answer()
    await db.user.update(
        call.from_user.id, {"language": f"{callback_data.language_code}"}
    )
    text = await db.user.get_languages_text(callback_data.language_code)
    try:
        await call.message.edit_text(
            text=text["updated_text"], reply_markup=None
        )
    except TelegramNotFound:
        pass

    start_text = await db.answer_texts.start_text(callback_data.language_code)
    await call.message.answer(text=start_text)
