import os
from aiogram.types import InputFile
from datetime import datetime
import asyncio

from aiogram import types

from data.config import ADMINS, SPREADSHEET_ID
from loader import dp, db, bot
from filters.is_privatechat import IsPrivateChat
import openpyxl


@dp.message_handler(IsPrivateChat(), text="/admin", user_id=ADMINS)
async def send_help_text(message: types.Message):
    content_text = "📝 Buyruqlar:"
    content_text += "\n\n<b>1. Buyruq:</b> /statistics\n<b>Tavsif:</b> Bot bo'yicha umumiy statistika ya'ni umumiy a'zolar soni, bir kunlik ro'yhatdan o'tgan foydalanuvchilar."
    content_text += "\n\n<b>2. Buyruq:</b> /excel\n<b>Tavsif:</b> Bot foydalanuvchilarning umumiy bazasini excel fayl ko'rinishida yuklab olish imkoniyati."
    content_text += "\n\n<b>2. Buyruq:</b> /google_sheet\n<b>Tavsif:</b> Bot foydalanuvchilarning umumiy bazasini google sheet'da ko'rinishi imkoniyati. "
    await message.answer(content_text)


@dp.message_handler(IsPrivateChat(), text="/statistics", user_id=ADMINS)
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


@dp.message_handler(IsPrivateChat(), text="/excel", user_id=ADMINS)
async def send_excel(message: types.Message):
    now = datetime.now()
    file_name = now.strftime("%H%M_%d%m%Y")
    now_date = now.strftime("%H:%M %d/%m/%Y")
    wb = openpyxl.load_workbook('example.xlsx')
    ws = wb.active
    users = await db.select_all_users()
    for indx, user in enumerate(users):
        user_data = (indx+1, user[1], user[2], user[3],
                     user[4], user[5], user[6], user[7])
        ws.append(user_data)

    file = f'{file_name}.xlsx'
    wb.save(file)

    caption = f"📝 Foydalanuvchilar umumiy ro'yhati\n\n{now_date} holatiga ko'ra."
    await bot.send_document(message.from_user.id, InputFile(file), caption=caption)
    os.remove(file)


@dp.message_handler(IsPrivateChat(), text="/google_sheet", user_id=ADMINS)
async def send_excel(message: types.Message):
    sheet_url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit#gid=261013140"
    text = "📝 Google sheet uchun link:"
    text += f"\n\n{sheet_url}"
    await message.answer(text)
