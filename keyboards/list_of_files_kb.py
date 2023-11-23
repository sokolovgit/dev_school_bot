
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def show_list_kb(file_list: list) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()

    adj = 1

    for i in file_list:

        if adj % 5 == 0:
            kb.adjust(5)

        kb.button(text=str(i))

        adj += 1

    kb.adjust(5)

    return kb.as_markup(resize_keyboard=True)

