from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, db
from keyboards.default.default_buttons import make_buttons
from states.register import Register


# Echo bot
@dp.message_handler(text="❌ Bekor qilish", state='*')
async def bot_echo(message: types.Message, state: FSMContext = '*'):
    user_id = message.from_user.id
    user = await db.select_user(telegram_id=user_id)
    if not user:
        await message.answer("❌ Jarayon bekor qilindi.\n\nQayta urinish uchun quyidagi tugmani ezing!", reply_markup=make_buttons(["Ro'yhatdan o'tish"]))
    else:
        await message.answer("❌ Jarayon bekor qilindi.", reply_markup=make_buttons(["Barcha suhbatlar (Himmat 700+)", "Ustozga savol yo'llash", "Asosiy guruhlar uchun link olish", "Taklif va e'tirozlar", "Ijtimoiy tarmoq havolalar"], row_width=1))
    await state.finish()
    await state.reset_data()
