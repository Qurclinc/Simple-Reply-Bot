from aiogram.fsm.state import State, StatesGroup

class AnswerMessage(StatesGroup):
    answer = State()
    
    
class Ban(StatesGroup):
    reason = State()