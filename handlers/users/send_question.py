from aiogram import types
from loader import dp, bot, db
from aiogram.dispatcher import FSMContext
from data.config import ADMINS

from filters.is_privatechat import IsPrivateChat
from states.sent_question import SendQuestionToTeacher
from keyboards.inline.buttons import confirmation_button
from keyboards.default.default_buttons import make_buttons


@dp.message_handler(IsPrivateChat(), text="Ustozga savol yo'llash")
async def bot_echo(message: types.Message):
    await message.answer("✏️ Savolingizni aniq ko'rinishda yozib jo'natishingiz mumkin:", reply_markup=make_buttons(["❌ Bekor qilish"]))
    await SendQuestionToTeacher.question.set()


@dp.message_handler(IsPrivateChat(), state=SendQuestionToTeacher.question)
async def bot_echo(message: types.Message, state: FSMContext):
    question_text = message.text
    await state.update_data(question_text=question_text)
    await message.answer(f"<i>{question_text}</i>\n\nBarchasi to'g'rimi, jo'natishim mumkinmi?", reply_markup=confirmation_button)
    await SendQuestionToTeacher.confirmation.set()


@dp.callback_query_handler(text_contains="yes_send", state=SendQuestionToTeacher.confirmation)
async def send_question(call: types.CallbackQuery, state: FSMContext):
    user = await db.select_user(telegram_id=call.from_user.id)
    full_name = user.get("full_name")
    username = user.get("username")
    question_data = await state.get_data()
    question_text = question_data.get("question_text")
    if username:
        send_text = f"📝 Ustozga savol yo'llandi.\n\n<b>Kimdan:</b> {full_name}\n<b>Telegam username:</b> @{username}\n\n<i>{question_text}</i>"
    for admin in ADMINS:
        await bot.send_message(chat_id=admin, text=send_text)
    await call.message.answer("✅ Savol muvaffaqiyatli yuborildi!", reply_markup=make_buttons(["Suhbatlar", "Ustozga savol yo'llash", "Dars uchun link olish", "Taklif va e'tirozlar", "Ijtimoiy tarmoq havolalar"], row_width=1))
    await call.answer(cache_time=60)
    await state.finish()


@dp.callback_query_handler(text_contains="no_send", state=SendQuestionToTeacher.confirmation)
async def send_question(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("📝 Savol bekor qilindi!", reply_markup=make_buttons(["Suhbatlar", "Ustozga savol yo'llash", "Dars uchun link olish", "Taklif va e'tirozlar", "Ijtimoiy tarmoq havolalar"], row_width=1))
    await call.answer(cache_time=60)
    await state.finish()
