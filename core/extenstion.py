from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from aiogram import Bot, Dispatcher
from .config import settings

engine = create_async_engine(
    settings.DB_URI,
    pool_size=5,     
    max_overflow=5,
    pool_pre_ping=True   
)
session_factory = async_sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False
)

bot = Bot(settings.TOKEN)
dp = Dispatcher()