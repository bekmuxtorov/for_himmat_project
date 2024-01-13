import asyncpg
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext

from loader import dp, db, bot
from data.config import ADMINS, CHANNELS
from states.register import Register
from filters.is_privatechat import IsPrivateChat

from keyboards.default.default_buttons import contact_request_button, make_buttons
from keyboards.inline.buttons import course_buttons


@dp.message_handler(IsPrivateChat(), CommandStart())
async def bot_start(message: types.Message):

    user = await db.select_user(telegram_id=message.from_user.id)
    if user:
        await message.answer("Marhamat o'zingizga kerakli guruhni tanlang: ", reply_markup=course_buttons)
    else: 
        await message.answer("Xush kelibsiz!\n\nBotdan foydalanish uchun quyidagi tugma yordamida ro'yhatdan o'ting!", reply_markup=make_buttons(["Ro'yhatdan o'tish"]))

    # ADMINGA xabar beramiz
    # count = await db.count_users()
    # msg = f"{user[1]} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
    # await bot.send_message(chat_id=ADMINS[0], text=msg)


@dp.callback_query_handler(text_contains="check_button")
async def is_member(call: types.CallbackQuery,):
    await call.message.delete()
    await call.message.answer(text="Barcha kanallarga a'zo bo'ldingiz! \n\nRo'yatdan o'tish uchun quyidagi tugmani bosing.", reply_markup=make_buttons(["Ro'yhatdan o'tish"]))
    await call.answer(cache_time=60)

