from aiogram import types
from loader import dp, db, bot

from filters.is_privatechat import IsPrivateChat
from keyboards.inline.buttons import talk_buttons
from keyboards.default import make_buttons


@dp.message_handler(IsPrivateChat(), text="Suhbatlar")
async def bot_echo(message: types.Message):
    titles = await db.get_titles()
    await message.answer("✅ Quyidan o'zingizga kerakli suhbatni tanglang:", reply_markup=talk_buttons(titles))


@dp.callback_query_handler(text_contains="talk_")
async def send_talk_link(call: types.CallbackQuery):
    talk_id = int(call.data.split('_')[1])
    chat_id = call.message.chat.id
    await call.message.delete()
    talk_data = await db.get_links(id=talk_id)
    title = talk_data.get("title")
    updated_at = talk_data.get("updated_at").strftime("%H:%M, %d/%m/%Y")
    text = f"💡 <b>Suhbat nomi:</b> {title}"
    text += f"\n⌚ <b>Yangilangan vaqti:</b> {updated_at}"
    links = talk_data.get("links")
    await call.message.answer(text=text, reply_markup=make_buttons(["❌ Bekor qilish"]))
    for link in links:
        await bot.send_audio(chat_id=chat_id, audio=link)
