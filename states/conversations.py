from aiogram.dispatcher.filters.state import State, StatesGroup


class ConversationState(StatesGroup):
    conversations = State()
