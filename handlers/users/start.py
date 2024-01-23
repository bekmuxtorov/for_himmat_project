import asyncpg
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext

from loader import dp, db, bot
from data.config import ADMINS, CHANNELS
from states.register import Register
from filters.is_privatechat import IsPrivateChat

from keyboards.default.default_buttons import contact_request_button, make_buttons
from keyboards.inline.buttons import course_button


@dp.message_handler(IsPrivateChat(), CommandStart())
async def bot_start(message: types.Message):

    user = await db.select_user(telegram_id=message.from_user.id)

    if user:
        full_name = user.get("full_name")
        await message.answer(f"Xurmatli {full_name}, marhamat o'zingizga kerakli guruhni tanlang: ", reply_markup=make_buttons(["Suhbatlar", "Ustozga savol yo'llash", "Dars uchun link olish", "Taklif va e'tirozlar", "Ijtimoiy tarmoq havolalar"], row_width=1))
    else:
        await message.answer("Xush kelibsiz!\n\nBotdan foydalanish uchun quyidagi tugma yordamida ro'yhatdan o'ting!", reply_markup=make_buttons(["Ro'yhatdan o'tish"]))


@dp.callback_query_handler(text_contains="check_button")
async def is_member(call: types.CallbackQuery,):
    user_id = call.from_user.id
    await call.message.delete()
    user = await db.select_user(telegram_id=user_id)
    if user:
        full_name = user.get("full_name")
        gender = user.get("gender")
        await call.message.answer(f"Xurmatli {full_name}, marhamat o'zingizga kerakli guruhni tanlang: ", reply_markup=course_button(gender))
        await call.answer(cache_time=60)
        return
    else:
        await call.message.answer(text="Barcha kanallarga a'zo bo'ldingiz! \n\nRo'yatdan o'tish uchun quyidagi tugmani bosing.", reply_markup=make_buttons(["Ro'yhatdan o'tish"]))
        return
