from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import Router, F, types
from aiogram.filters import Command

from bot.filters import IsBlocked, IsAdmin
from core.config import settings
from core.extenstion import bot
from bot.keyboards.admin import reply_keyboard

router = Router()

@router.message(Command("start"))
async def start(message: types.Message):
    await message.answer(settings.GREETINGS_TEXT, reply_markup=types.ReplyKeyboardRemove())
    
@router.message(F.text, ~IsBlocked(), ~IsAdmin())
async def send_message(message: types.Message, session: AsyncSession):
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
        
        await message.reply("Сообщение отправлено!")
    except Exception:
        await message.reply("Не удалось отправить сообщение")