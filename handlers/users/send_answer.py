from datetime import timedelta
from aiogram import types
from loader import dp, bot, db
from aiogram.dispatcher import FSMContext

from data.config import ADMIN_GROUP_ID
from states.sent_question import AnswerToUser
from keyboards.inline.buttons import confirmation_button
from keyboards.default.default_buttons import make_buttons, build_menu_buttons
from filters.is_privatechat import IsPrivateChat, IsPrivateChatForCallback
from utils.db_api.build_message_group import build_message_group


async def writing_answer(message: types.Message, payload: str, state: FSMContext):
    question_id = payload.split(':')[1]
    user = await db.select_user(telegram_id=message.from_user.id)
    question_data = await db.select_question(id=int(question_id))
    question_text = question_data.get("body")
    for_who = question_data.get("for_who")
    is_registered, send_text = await build_message_group(message=message, user=user, question_text=question_text, for_who=for_who)
    msg_question = await message.answer(text=send_text)
    text = "Quyida javobingizni yozishingiz mumkin:"
    msg = await message.answer(text=text, reply_markup=make_buttons(["❌ Bekor qilish"]))
    await state.update_data(question_id=question_id)
    await state.update_data(message_id=msg.message_id)
    await state.update_data(message_question_id=msg_question.message_id)
    await AnswerToUser.answer.set()


@dp.message_handler(IsPrivateChat(), state=AnswerToUser.answer)
async def reply_question(message: types.Message, state: FSMContext):
    data = await state.get_data()
    old_message_id = data.get("message_id")
    message_question_id = data.get("message_question_id")
    await bot.delete_message(chat_id=message.from_user.id, message_id=int(old_message_id))
    await bot.delete_message(chat_id=message.from_user.id, message_id=int(message_question_id))
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    answer_text = message.text
    await state.update_data(answer_text=answer_text)
    text = f"<i>{answer_text}</i>\n\nJavob yuborilsinmi?"
    await message.answer(text=text, reply_markup=confirmation_button)
    await AnswerToUser.confirmation.set()


@dp.callback_query_handler(IsPrivateChatForCallback(), text_contains="yes_send", state=AnswerToUser.confirmation)
async def send_question(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    answer_details = await state.get_data()
    answer_text = answer_details.get("answer_text")
    question_id = answer_details.get("question_id")

    question_data = await db.select_question(id=int(question_id))
    question_body = question_data.get("body")
    question_sender_id = question_data.get("sender_user_id")
    created_at = (question_data.get(
        "created_at") + timedelta(hours=5)) .strftime("%H:%M, %d/%m/%Y")

    text = f"✅ Savolga javob yo'llandi.\n\n"
    text += f"<b>Yuborilgan vaqt:</b> {created_at}\n"
    text += f"<b>Savol:</b> <i> {question_body}</i>\n\n"
    text += f"<b>Yo'llangan javob:</b><i> {answer_text}</i>"

    await db.update_question_answer(answer=answer_text, question_id=int(question_id))
    await bot.send_message(chat_id=question_sender_id, text=text)
    await bot.send_message(chat_id=ADMIN_GROUP_ID, text=text)
    await call.message.answer(text="✅ Javob muvaffaqiyatli yuborildi!", reply_markup=build_menu_buttons)
    await call.answer(cache_time=60)
    await state.finish()
    await state.reset_data()


@dp.callback_query_handler(IsPrivateChatForCallback(), text_contains="no_send", state=AnswerToUser.confirmation)
async def send_question(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(text="📝 Jo'natish bekor qilindi!", reply_markup=build_menu_buttons)
    await call.answer(cache_time=60)
    await state.finish()
    await state.reset_data()


# @dp.message_handler(content_types=types.ContentTypes.ANY)
# async def admin_reply(message: types.Message):
#     if isinstance(message.reply_to_message, types.Message):
#         reply_m = message.reply_to_message
#         if reply_m.forward_from and reply_m.forward_from.id:
#             await message.copy_to(reply_m.forward_from.id, reply_markup=message.reply_markup)
#         else:
#             message_id_ = reply_m.message_id
#             chat_id = db.get_message_chat_id(message_id_)
#             await message.copy_to(chat_id, reply_markup=message.reply_markup)
#     else:
#         pass
