from aiogram import Router, F, types
from aiogram.filters import Command

from filters import IsBlocked, IsAdmin
from config import settings, bot
from keyboards.admin import reply_keyboard

router = Router()

@router.message(Command("start"))
async def start(message: types.Message):
    await message.answer(settings.GREETINGS_TEXT)
    
@router.message(F.text, ~IsBlocked(), ~IsAdmin())
async def send_message(message: types.Message):
    try:
        username = message.from_user.username
        if username:
            content = f"@{username}\n\n{message.text[:4000]}"
        else:
            content = message.text[:4000]
        await bot.send_message(
            chat_id=settings.ADMIN_ID,
            text=content,
            reply_markup=await reply_keyboard(int(message.from_user.id))
        )
        
        await message.answer("Сообщение отправлено!")
    except Exception:
        await message.answer("Не удалось отправить сообщение")
        
@router.message(F.text, IsBlocked(), ~IsAdmin())
async def notify_banned(message: types.Message):
    await message.answer("Вас заблокировали в боте.")