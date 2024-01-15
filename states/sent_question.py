from aiogram.dispatcher.filters.state import State, StatesGroup


class SendQuestionToTeacher(StatesGroup):
    question = State()
    confirmation = State()


class SendQuestionToAdmin(StatesGroup):
    question = State()
    confirmation = State()