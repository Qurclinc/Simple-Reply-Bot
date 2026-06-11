from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.filters import BaseFilter
from aiogram.types import Message

from core.crud import blacklist_crud

class IsBlocked(BaseFilter):
    
    async def __call__(self, message: Message, session: AsyncSession):
        user_id = message.from_user.id
        result = await blacklist_crud.get_user(user_id, session)
        return result is not None