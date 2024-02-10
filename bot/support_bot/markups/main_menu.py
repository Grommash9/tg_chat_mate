from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


class LanguageCallback(CallbackData, prefix="locale"):
    action: str
    language_code: str


def choosing_language(language_info):
    m = InlineKeyboardBuilder()
    for info in language_info:
        m.button(
            text=f"{info.get('change_text')}",
            callback_data=LanguageCallback(
                action="set_language",
                language_code=f"{info.get('language_code')}",
            ),
        )
    return m.adjust(3).as_markup()
