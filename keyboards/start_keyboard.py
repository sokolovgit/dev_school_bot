from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def choose_action_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Download file")
    kb.button(text="Send downloaded file")
    kb.button(text="Send file from url")
    kb.adjust(3)
    return kb.as_markup(resize_keyboard=True)


