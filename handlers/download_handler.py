import logging
import re
import os

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State

from keyboards.start_keyboard import choose_action_kb

save_path = "/Users/qwertannov/Documents/python/bot_ht6/files/"

router = Router()


class UserState(StatesGroup):
    downloading = State()
    downloading_photo = State()
    downloading_video = State()


def is_valid_filename(name: str) -> bool:
    pattern = r'^[a-zA-Z0-9_-]+$'
    return bool(re.match(pattern, name))


@router.message(Command("download"))
@router.message(F.text.lower() == "download file")
async def cmd_download(message: Message, state: FSMContext):
    await message.answer("*Please send your document or media*")
    await state.set_state(UserState.downloading)


@router.message(F.photo, UserState.downloading)
async def get_photo_info(message: Message, state: FSMContext):
    await state.set_state(UserState.downloading_photo)
    await state.update_data(file_id=message.photo[-1].file_id)
    await message.answer("*Please enter name for the photo:*")


@router.message(UserState.downloading)
async def invalid_input(message: Message, state: FSMContext):
    await message.answer("Invalid input\.")
    await message.answer(text="*Choose what you want to do*", reply_markup=choose_action_kb())
    await state.clear()


@router.message(F.text, UserState.downloading_photo)
async def download_photo(message: Message, bot: Bot, state: FSMContext):

    if is_valid_filename(message.text):
        name = message.text
    else:
        await message.answer("_Invalid name for the file\!_")
        return

    user_data = await state.get_data()

    user_directory = str(message.from_user.id)
    path = f"{save_path}{user_directory}/"

    try:
        os.mkdir(path)
    except:
        logging.info("Directory for user didn't created. It is already exists")

    await bot.download(user_data['file_id'],
                       destination=f"{path}{name}.png")
    await message.answer(f"*File has been successfully downloaded as* _{name}\.png_")
    await state.clear()


@router.message(F.video, UserState.downloading)
async def get_video_info(message: Message, state: FSMContext):
    await state.set_state(UserState.downloading_video)
    await state.update_data(file_id=message.video.file_id)
    await message.answer("*Please enter name for the video:*")


@router.message(UserState.downloading)
async def invalid_input(message: Message, state: FSMContext):
    await message.answer("Invalid input\.")
    await state.clear()
    await message.answer(text="*Choose what you want to do*", reply_markup=choose_action_kb())


@router.message(F.text, UserState.downloading_video)
async def download_video(message: Message, bot: Bot, state: FSMContext):

    if is_valid_filename(message.text):
        name = message.text
    else:
        await message.answer("_Invalid name for the file\!_")
        return

    user_data = await state.get_data()

    user_directory = str(message.from_user.id)
    path = f"{save_path}{user_directory}/"

    try:
        os.mkdir(path)
    except:
        logging.info("Directory for user didn't created. It is already exists")

    await bot.download(user_data['file_id'],
                       destination=f"{path}{name}.mp4")
    await message.answer(f"*File has been successfully downloaded as* _{name}\.mp4_")
    await state.clear()


@router.message(F.document)
async def download_document(message: Message, bot: Bot):

    user_directory = str(message.from_user.id)
    path = f"{save_path}{user_directory}/"

    try:
        os.mkdir(path)
    except:
        logging.info("Directory for user didn't created. It is already exists")

    await bot.download(
        message.document,
        destination=f"{path}{message.document.file_name}")
    await message.answer("*File has been successfully downloaded\!*")

