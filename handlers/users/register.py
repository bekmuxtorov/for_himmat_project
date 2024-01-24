from utils.db_api.write_google_sheet import write_range
from datetime import datetime as dt
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
import pytz

from loader import dp, db, bot
from states.register import Register
from filters.is_privatechat import IsPrivateChat

from keyboards.default.default_buttons import contact_request_button, make_buttons
from keyboards.inline.buttons import course_button


@dp.message_handler(IsPrivateChat(), text="Ro'yhatdan o'tish")
async def register(message: types.Message, state: FSMContext):
    await message.answer(text="Ism familiyangizni kiriting:\n\nNamuna: Palonchiyev Pistonchi", reply_markup=make_buttons(['❌ Bekor qilish',]))
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
    await message.answer(text="Jinsingizni tanglang:", reply_markup=make_buttons(["Erkak", "Ayol", "❌ Bekor qilish"], row_width=2))
    await Register.gender.set()


@dp.message_handler(IsPrivateChat(), state=Register.phone_number)
async def register(message: types.Message, state: FSMContext):
    await message.answer("Iltimos telefon raqamingizni quyidagi tugma yordamida ulashing!", reply_markup=contact_request_button)
    await Register.phone_number.set()


@dp.message_handler(IsPrivateChat(), state=Register.gender)
async def register(message: types.Message, state: FSMContext):
    gender = message.text
    if gender not in ("Erkak", "Ayol"):
        await message.answer("Iltimos quyidagi tugmalardan biri tanglang: ", reply_markup=make_buttons(["Erkak", "Ayol", "❌ Bekor qilish"], row_width=2))
        await Register.gender.set()
        return

    await state.update_data(gender=gender)
    await message.answer(text="Yoshingizni kiriting:\n\nNamuna: 22", reply_markup=make_buttons(["❌ Bekor qilish"]))
    await Register.age.set()


@dp.message_handler(IsPrivateChat(), state=Register.age)
async def register(message: types.Message, state: FSMContext):
    age = message.text
    user_data = await state.get_data()
    # user_data["age"] = age
    # user_data["user_id"] = message.from_user.id
    user_id = message.from_user.id
    username = message.from_user.username
    full_name = user_data.get("full_name")
    phone_number = user_data.get("phone_number")
    gender = user_data.get("gender")
    create_at = dt.now(pytz.timezone('Asia/Tashkent')).strftime("%H:%M, %d/%m/%Y")

    try:
        await db.add_user(
            full_name=full_name,
            username=username,
            telegram_id=user_id,
            phone_number=phone_number,
            gender=gender,
            age=age
        )
        await message.answer(text="Siz muaffaqqiyatli ro'yhatdan o'tdingiz, \n\nQuyidagi tugmalardan birini tanglashingiz va guruhga qo'shilishingiz mumkin.", reply_markup=course_button(gender))
        await write_range([full_name, username, user_id,
                           phone_number, gender, age, create_at])
        await state.finish()
    except:
        await message.answer(text="Ro'yhatdan o'tishda qandaydir muammo chiqdi, iltimos qayta urinib ko'ring!", reply_markup=make_buttons(["Ro'yhatdan o'tish"]))
        await state.finish()
