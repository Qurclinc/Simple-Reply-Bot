from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from core.extenstion import bot
from bot.states import AnswerMessage, Ban
from bot.filters import IsAdmin
from bot.keyboards.admin import back
from core.crud import blacklist_crud

router = Router()

# Ответ на сообщения
# -------------------------------------------
@router.callback_query(IsAdmin(), F.data.startswith("answer"))
async def answer(callback: types.CallbackQuery, state: FSMContext):
    uid = int(callback.data.split(":")[1])
    await state.set_data({"uid": uid})
    await callback.message.reply("Напишите сообщение", reply_markup=await back())
    await state.set_state(AnswerMessage.answer)
    
@router.message(AnswerMessage.answer)
async def send_answer(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        await bot.send_message(
            chat_id=data.get("uid"),
            text=message.text[:4096]
        )
    except Exception:
        await message.reply("Не удалось ответить.")
        return
    await message.reply("Ответ успешно отправлен.")
    await state.clear()

@router.callback_query(F.data.startswith("cancel"))
async def cancel(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Отмена...")
    await state.clear()
    
    
# Бан/разбан пользователей
# -------------------------------------------
@router.callback_query(F.data.startswith("ban"))
async def ban(callback: types.CallbackQuery, state: FSMContext):
    uid = int(callback.data.split(":")[1])
    await state.set_data({"user_id": uid})
    await callback.message.answer("Укажите причину бана:", reply_markup=await back())
    await state.set_state(Ban.reason)
    
@router.message(Ban.reason)
async def perform_ban(message: types.Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    reason = message.text[:2048]
    try:
        result = await blacklist_crud.ban_user(
            user_id=data["user_id"],
            reason=reason,
            session=session
        )
    except Exception:
        await message.answer("Не удалось забанить пользователя")
        return
    if result:
        try:
            await bot.send_message(
                chat_id=data["user_id"],
                text=f"Вы были заблокированы.\nПричина: {reason}"
            )
            await message.reply("Пользователь успешно заблокирован.")
        except Exception:
            pass
    await state.clear()
    
@router.message(Command("unban"), IsAdmin())
async def unban_user(message: types.Message, session: AsyncSession):
    try:
        user_id = int(message.text.split()[-1])
    except Exception:
        await message.reply("Неверный ID!")
        return
    result = await blacklist_crud.unban_user(user_id, session)
    if result:
        await message.reply("Пользователь успешно разблокирован")
    else:
        await message.reply("Не удалось разблокировать пользователя")
        
    try:
        await bot.send_message(
            chat_id=user_id,
            text="Вы были разблокированы. Можете снова писать сообщения."
        )
    except Exception:
        pass