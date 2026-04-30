import json
import os
from aiogram.filters import BaseFilter
from aiogram.types import Message
from config import settings

class IsBlocked(BaseFilter):
    def __init__(self):
        if (not(os.path.exists(settings.BLACKLIST_FILEPATH))):
            with open(settings.BLACKLIST_FILEPATH, "w") as f:
                f.write("[]")
        self._blocked_users = set()
        self._file_mtime = 0
        self._load_if_changed()
        super().__init__()
    
    def _load_if_changed(self):
        current_mtime = os.path.getmtime(settings.BLACKLIST_FILEPATH)
        if current_mtime != self._file_mtime:
            with open(settings.BLACKLIST_FILEPATH, "r") as f:
                self._blocked_users = set(json.load(f))
            self._file_mtime = current_mtime
    
    async def __call__(self, message: Message):
        self._load_if_changed()
        return message.from_user.id in self._blocked_users