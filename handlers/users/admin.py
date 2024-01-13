import asyncio

from aiogram import types

from data.config import ADMINS
from loader import dp, db, bot

@dp.message_handler(text="/admin", user_id=ADMINS)
async def send_help_text(message: types.Message):
    content_text = "📝 Buyruqlar:"
    content_text += "\n\n<b>1. Buyruq:</b> /statistics\n<b>Tavsif:</b> Bot bo'yicha umumiy statistika ya'ni umumiy a'zolar soni, bir kunlik ro'yhatdan o'tgan foydalanuvchilar."
    content_text += "\n\n<b>2. Buyruq:</b> /excel\n<b>Tavsif:</b> Bot foydalanuvchilarning umumiy bazasini excel fayl ko'rinishida yuklab olish imkoniyati."
    await message.answer(content_text)


@dp.message_handler(text="/statistics", user_id=ADMINS)
async def send_statistics(message: types.Message):
    counts = {
        "Barcha userlar soni": await db.count_users(),
        "Erkaklar soni": await db.count_man_users(),
        "Ayollar soni": await db.count_woman_users(),
        "Bugun ro'yhatdan o'tganlar soni": await db.count_users_by_time()
    }

    content_text = "📝 Umumiy statistika:\n\n"

    for title, count in counts.items():
        content_text += f"<b>{title}</b>: {count} ta\n\n"
    await message.answer(content_text)