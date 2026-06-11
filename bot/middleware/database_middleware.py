from typing import Callable, Dict, Any, Awaitable

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self.session_factory = session_factory
        
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        async with self.session_factory() as session:
            data["session"] = session
            try:
                return await handler(event, data)
            except Exception as ex:
                print(str(ex))
                # Откат сессии в случае ошибки, чтобы оно не вызвало ещё ошибок
                await session.rollback()