import json
from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import bot, settings
from filters import IsAdmin
from keyboards.admin import back

router = Router()

class AnswerMessage(StatesGroup):
    answer = State()
    
@router.callback_query(IsAdmin(), F.data.startswith("answer"))
async def answer(callback: types.CallbackQuery, state: FSMContext):
    uid = int(callback.data.split(":")[1])
    await state.set_data({"uid": uid})
    await callback.message.answer("Напишите сообщение", reply_markup=await back())
    await state.set_state(AnswerMessage.answer)
    
@router.message(AnswerMessage.answer)
async def send_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await bot.send_message(
        chat_id=data.get("uid"),
        text=message.text[:4096]
    )
    await state.clear()

@router.callback_query(F.data.startswith("cancel"))
async def cancel(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Отмена...")
    await state.clear()
    
    
@router.callback_query(F.data.startswith("ban"))
async def ban(callback: types.CallbackQuery):
    uid = int(callback.data.split(":")[1])
    with open(settings.BLACKLIST_FILEPATH, "r") as fin:
        blocked_users = json.load(fin)
    if uid in blocked_users:
        await callback.message.answer("Пользователь уже в чёрном списке")
        return
    blocked_users.append(uid)
    
    with open(settings.BLACKLIST_FILEPATH, "w") as fout:
        json.dump(blocked_users, fout)
        await callback.message.answer("Пользователь забанен")