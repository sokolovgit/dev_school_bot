import os

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State

from keyboards.list_of_files_kb import show_list_kb
from keyboards.start_keyboard import choose_action_kb
from handlers.download_handler import save_path

router = Router()


class UserState(StatesGroup):
    choosing_file = State()


@router.message(Command("upload"))
@router.message(F.text.lower() == "send downloaded file")
async def show_list(message: Message, state: FSMContext):

    if not os.path.exists(f"{save_path}{message.from_user.id}/"):
        await message.answer("You haven't downloaded any files, so you can't upload any from bot\. "
                             "Please firstly download something before uploading")
        await message.answer(text='*Choose what you want to do*', reply_markup=choose_action_kb())
        return

    files = os.listdir(f"{save_path}{message.from_user.id}/")

    if not files:
        await message.answer("Your list is emty\. Please download something before uploading")
        await message.answer(text='*Choose what you want to do*', reply_markup=choose_action_kb())
        return

    await message.answer(text="*Your list is:*", reply_markup=show_list_kb(files))
    await state.set_state(UserState.choosing_file)


@router.message(F.text, UserState.choosing_file)
async def send_file(message: Message, state: FSMContext):

    files = os.listdir(f"{save_path}{message.from_user.id}/")

    if message.text not in files:
        await message.answer("*There is no such file in a list\!*")
        return

    file_from_pc = FSInputFile(f"{save_path}{message.from_user.id}/{message.text}")
    await message.answer_document(file_from_pc, reply_markup=ReplyKeyboardRemove())
    await state.clear()
    await message.answer(text='*Choose what you want to do*', reply_markup=choose_action_kb())
