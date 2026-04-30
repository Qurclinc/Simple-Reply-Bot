from aiogram.filters import BaseFilter
from aiogram.types import Message

from config import settings

class IsAdmin(BaseFilter):
    def __init__(self):
        self.admin_id = settings.ADMIN_ID
        super().__init__()
    
    async def __call__(self, message: Message):
        return message.from_user.id == self.admin_id