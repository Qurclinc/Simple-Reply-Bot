from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def reply_keyboard(uid: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Ответить", callback_data=f"answer:{uid}"),
        InlineKeyboardButton(text="Заблокировать", callback_data=f"ban:{uid}")]
    ])
    
async def back():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Отмена", callback_data="cancel")]
    ])