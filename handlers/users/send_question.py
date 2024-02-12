from filters.is_privatechat import IsPrivateChatForCallback
from aiogram import types
from loader import dp, bot, db
from aiogram.dispatcher import FSMContext
from data.config import ADMINS, ADMIN_GROUP_ID

from filters.is_privatechat import IsPrivateChat
from states.sent_question import SendQuestionToTeacher, AnswerToUser
from keyboards.inline.buttons import confirmation_button, reply_buttons
from keyboards.default.default_buttons import make_buttons, build_menu_buttons, not_registered_for_menu_buttons
from utils.db_api.build_message_group import build_message_group


@dp.message_handler(IsPrivateChat(), text="📝 Ustozga savol yo'llash 📝")
async def bot_echo(message: types.Message):
    await message.answer("✏️ Savol jo'natishingiz mumkin:", reply_markup=make_buttons(["❌ Bekor qilish"]))
    await SendQuestionToTeacher.question.set()


@dp.message_handler(IsPrivateChat(), state=SendQuestionToTeacher.question)
async def bot_echo(message: types.Message, state: FSMContext):
    question_text = message.text
    await state.update_data(question_text=question_text)
    await message.answer(f"<i>{question_text}</i>\n\nBarchasi to'g'rimi, jo'natishim mumkinmi?", reply_markup=confirmation_button)
    await SendQuestionToTeacher.confirmation.set()


@dp.callback_query_handler(IsPrivateChatForCallback(), text_contains="yes_send", state=SendQuestionToTeacher.confirmation)
async def send_question(call: types.CallbackQuery, state: FSMContext):
    question_data = await state.get_data()
    question_text = question_data.get("question_text")
    await call.message.delete()
    user = await db.select_user(telegram_id=call.from_user.id)
    is_registered, send_text = await build_message_group(message=call, user=user, question_text=question_text)
    question_id = await db.add_question(call.from_user.id, question_text)
    await bot.send_message(chat_id=ADMIN_GROUP_ID, text=send_text, reply_markup=await reply_buttons(question_id))

    text = "✅ Savol muvaffaqiyatli yuborildi!"
    if is_registered:
        await call.message.answer(text=text, reply_markup=build_menu_buttons)
    else:
        await call.message.answer(text=text, reply_markup=not_registered_for_menu_buttons)

    await call.answer(cache_time=60)
    await state.finish()


@dp.callback_query_handler(IsPrivateChatForCallback(), text_contains="no_send", state=SendQuestionToTeacher.confirmation)
async def send_question(call: types.CallbackQuery, state: FSMContext):
    user = await db.select_user(telegram_id=call.from_user.id)
    text = "📝 Savol bekor qilindi!"
    await call.message.delete()

    if user:
        await call.message.answer(text=text, reply_markup=build_menu_buttons)
    else:
        await call.message.answer(text=text, reply_markup=not_registered_for_menu_buttons)

    await call.answer(cache_time=60)
    await state.finish()
