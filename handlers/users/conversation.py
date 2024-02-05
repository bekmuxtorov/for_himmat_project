from aiogram import types
from loader import dp, db, bot

from filters.is_privatechat import IsPrivateChat
from keyboards.default import make_buttons, build_talk_buttons
from states.conversations import ConversationState
from aiogram.dispatcher import FSMContext


@dp.message_handler(IsPrivateChat(), text="🔙 Ortga qaytish", state='*')
@dp.message_handler(IsPrivateChat(), text="📚 Barcha suxbatlar(Himmat 700+) 📚")
async def bot_echo(message: types.Message, state: FSMContext):
    await state.finish()
    await state.reset_data()
    titles = await db.get_titles()
    await message.answer("✅ Quyidan o'zingizga kerakli suhbatni tanglang:", reply_markup=build_talk_buttons(titles))
    await ConversationState.conversations.set()


@dp.message_handler(state=ConversationState.conversations)
async def send_talk_link(message: types.Message, state):
    title = message.text
    await message.delete()
    titles = await db.get_titles()
    talk_id = list(titles.keys())[list(titles.values()).index(title)]
    chat_id = message.chat.id
    talk_data = await db.get_links(id=talk_id)
    updated_at = talk_data.get("updated_at").strftime("%H:%M, %d/%m/%Y")

    text = f"💡 <b>Suhbat nomi:</b> {title}"
    text += f"\n⌚ <b>Yangilangan vaqti:</b> {updated_at}"
    links = talk_data.get("links")
    await message.answer(text=text, reply_markup=make_buttons(["🔙 Ortga qaytish"]))
    for idx, link in enumerate(links):
        caption = f"{title} - {idx+1} suxbat"
        await bot.send_audio(chat_id=chat_id, audio=link, caption=caption)
    await state.finish()
    await message.answer(text=f"✅ {title} bo'yicha barcha suhbatlar yuborildi.", reply_markup=make_buttons(["🔙 Ortga qaytish"]))


# @dp.callback_query_handler(text_contains="talk_")
# async def send_talk_link(call: types.CallbackQuery):
#     talk_id = int(call.data.split('_')[1])
#     chat_id = call.message.chat.id
#     await call.message.delete()
#     talk_data = await db.get_links(id=talk_id)
#     title = talk_data.get("title")
#     updated_at = talk_data.get("updated_at").strftime("%H:%M, %d/%m/%Y")

#     text = f"💡 <b>Suhbat nomi:</b> {title}"
#     text += f"\n⌚ <b>Yangilangan vaqti:</b> {updated_at}"
#     links = talk_data.get("links")
#     await call.message.answer(text=text, reply_markup=make_buttons(["🏠 Bosh sahifa"]))
#     for idx, link in enumerate(links):
#         caption = f"{title} - {idx+1} suxbat"
#         await bot.send_audio(chat_id=chat_id, audio=link, caption=caption)
