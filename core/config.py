from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    TOKEN: str
    ADMIN_ID: int
    # BLACKLIST_FILEPATH: str = str(Path(__file__).parent / "blacklist.json")
    GREETINGS_TEXT: str = """Здравствуйте. Напишите сообщение, и Вам обязательно вскоре ответят. ^^"""
    
    @property
    def DB_URI(self):
        return "sqlite+aiosqlite:///blacklist.db"
    
    @property
    def SYNC_DB_URI(self):
        return "sqlite:///blacklist.db"
    
    
settings = Settings()