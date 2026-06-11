# import logging
import asyncio
from aiogram import types
from aiogram.utils.callback_answer import CallbackAnswerMiddleware

from core.config import settings
from core.extenstion import bot, dp, session_factory
from bot.handlers import admin_router, user_router
from bot.middleware.database_middleware import DatabaseMiddleware

dp.update.outer_middleware(DatabaseMiddleware(session_factory=session_factory))
dp.callback_query.outer_middleware(DatabaseMiddleware(session_factory=session_factory))
dp.callback_query.middleware(CallbackAnswerMiddleware())


# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
#     datefmt="%d-%m-%Y %H:%M:%S"
# )

async def main():
    await bot.set_my_commands(
        commands=[
            types.BotCommand(command="unban", description="/unban <user_id>"),
        ],
        scope=types.bot_command_scope_chat.BotCommandScopeChat(chat_id=settings.ADMIN_ID)
    )
    dp.include_routers(admin_router, user_router)
    print("bot is running...")
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())