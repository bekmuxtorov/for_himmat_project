import asyncpg
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext

from loader import dp, db, bot
from data.config import ADMINS, CHANNELS
from states.register import Register
from filters.is_privatechat import IsPrivateChat


@dp.message_handler(IsPrivateChat(), CommandStart())
async def bot_start(message: types.Message):
    try:
        user = await db.add_user(telegram_id=message.from_user.id,
                                 full_name=message.from_user.full_name,
                                 username=message.from_user.username)
    except asyncpg.exceptions.UniqueViolationError:
        user = await db.select_user(telegram_id=message.from_user.id)

    await message.answer("Xush kelibsiz!")

    # ADMINGA xabar beramiz
    count = await db.count_users()
    msg = f"{user[1]} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
    await bot.send_message(chat_id=ADMINS[0], text=msg)


@dp.callback_query_handler(text_contains="check_button")
async def is_member(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(text="Barcha kanallarga a'zo bo'ldingiz! \n\nIsm familiyangizni kiriting!")
    await call.answer(cache_time=60)
    await Register.full_name.set()


@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    await message.answer(message.text)
