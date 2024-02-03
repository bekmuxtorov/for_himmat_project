import asyncpg
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext

from loader import dp, db, bot
from data.config import ADMINS, CHANNELS
from states.register import Register
from filters.is_privatechat import IsPrivateChat

from keyboards.default.default_buttons import make_buttons, build_menu_buttons
from keyboards.inline.buttons import course_button


@dp.message_handler(IsPrivateChat(), CommandStart())
async def bot_start(message: types.Message):

    user = await db.select_user(telegram_id=message.from_user.id)

    if user:
        full_name = user.get("full_name")
        await message.answer(f"Xurmatli {full_name}, marhamat o'zingizga kerakli bo'limni tanlang: ", reply_markup=build_menu_buttons)
    else:
        await message.answer("Xush kelibsiz!\n\nBotdan foydalanish uchun quyidagi tugma yordamida ro'yhatdan o'ting!", reply_markup=make_buttons(["Ro'yhatdan o'tish"]))


@dp.callback_query_handler(text_contains="check_button")
async def is_member(call: types.CallbackQuery,):
    user_id = call.from_user.id
    await call.message.delete()
    if call.message.chat.type in (types.ChatType.SUPERGROUP, types.ChatType.GROUP):
        await call.message.answer("💡 Guruhdan foydalanishingiz mumkin!")
        return
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


@dp.callback_query_handler(text="million_course")
async def million_course(call: types.CallbackQuery):
    await call.message.delete()
    text = "🔔 Hozircha Millionerlar klubiga qabul to'xtatilgan, qabul ochilishi bilan sizga xabar beramiz!"
    await call.message.answer(text=text, reply_markup=build_menu_buttons)
