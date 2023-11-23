from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.start_keyboard import choose_action_kb

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="*Chose what you want to do:*",
        reply_markup=choose_action_kb())


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="_Action is cancelled_",
        reply_markup=ReplyKeyboardRemove())
    await message.answer(text="*Choose what you want to do*", reply_markup=choose_action_kb())


@router.message(StateFilter(None))
async def invalid_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("*Unknown command\.*")
    await message.answer(text="*Choose what you want to do*", reply_markup=choose_action_kb())