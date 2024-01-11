import asyncpg
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext

from loader import dp, db, bot
from data.config import ADMINS, CHANNELS
from states.register import Register
from filters.is_privatechat import IsPrivateChat

from keyboards.default.default_buttons import contact_request_button, make_buttons


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


@dp.message_handler(IsPrivateChat(), state=Register.full_name)
async def bot_echo(message: types.Message, state: FSMContext):
    full_name = message.text
    await state.update_data(full_name=full_name)
    await message.answer(text="Telefon raqamingizni kiriting:", reply_markup=contact_request_button)
    await Register.phone_number.set()


@dp.message_handler(IsPrivateChat(), state=Register.phone_number, content_types="contact")
async def register(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number
    await state.update_data(phone_number=phone_number)
    await message.answer(text="Jinsingizni tanglang:", reply_markup=make_buttons(["Erkak", "Ayol"], row_width=2))
    await Register.gender.set()


@dp.message_handler(IsPrivateChat(), state=Register.gender)
async def register(message: types.Message, state: FSMContext):
    gender = message.text
    await state.update_data(gender=gender)
    await message.answer(text="Yoshingizni kiriting:\n\nNamuna: 22")
    await Register.age.set()


@dp.message_handler(IsPrivateChat(), state=Register.age)
async def register(message: types.Message, state: FSMContext):
    age = message.text
    user_data = await state.get_data()
    user_data["age"] = age
    user_data["user_id"] = message.from_user.id
    user_id = message.from_user.id
    full_name = user_data.get("full_name")
    phone_number = user_data.get("phone_number")
    gender = user_data.get("gender")

    print(user_data)
