from pathlib import Path

from aiogram import Bot, Dispatcher
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    TOKEN: str
    ADMIN_ID: int
    BLACKLIST_FILEPATH: str = str(Path(__file__).parent / "blacklist.json")
    GREETINGS_TEXT: str = """Здравствуйте. Напишите сообщение, и вам обязательно вскоре ответят. ^^"""
    
settings = Settings()

bot = Bot(settings.TOKEN)
dp = Dispatcher()