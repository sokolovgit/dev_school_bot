import validators
import requests

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, URLInputFile
from aiogram.fsm.state import StatesGroup, State

from keyboards.start_keyboard import choose_action_kb


router = Router()


class UserState(StatesGroup):
    sending_url = State()


@router.message(Command("url_upload"))
@router.message(F.text.lower() == "send file from url")
async def url_upload(message: Message, state: FSMContext):
    await state.set_state(UserState.sending_url)
    await message.answer("*Please send your url*")


@router.message(UserState.sending_url, F.text)
async def send_url_photo(message: Message, state: FSMContext):

    if not validators.url(message.text):
        await message.answer("_Invalid URL\!_")
        return

    url = message.text

    response = requests.head(url)

    if 'image' not in response.headers.get('content-type', '').lower():
        await message.answer("_There is no image in the URL\!_")
        return

    image_from_url = URLInputFile(url)

    await message.answer_photo(image_from_url)
    await state.clear()
    await message.answer(text='*Choose what you want to do*', reply_markup=choose_action_kb())


@router.message(UserState.sending_url)
async def message_send_incorrectly(message: Message):
    await message.answer("_That's not an URL\!_")

