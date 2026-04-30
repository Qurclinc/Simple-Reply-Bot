import asyncio

from config import settings, bot, dp
from handlers import admin_router, user_router

async def main():
    dp.include_routers(admin_router, user_router)
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())