from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, db
from keyboards.default.default_buttons import make_buttons


# Echo bot
@dp.callback_query_handler(text_contains="home_page", state='*')
async def bot_echo(call: types.CallbackQuery, state: FSMContext = '*'):
    user_id = call.from_user.id
    user = await db.select_user(telegram_id=user_id)
    if not user:
        await call.message.answer("Xush kelibsiz!\n\nBotdan foydalanish uchun quyidagi tugma yordamida ro'yhatdan o'ting!", reply_markup=make_buttons(["Ro'yhatdan o'tish"]))
    else:
        await call.message.answer("🏠 Bosh sahifa", reply_markup=make_buttons(["Barcha suhbatlar (Himmat 700+)", "Ustozga savol yo'llash", "Asosiy guruhlar uchun link olish", "Taklif va e'tirozlar", "Ijtimoiy tarmoq havolalar"], row_width=1))
    await state.finish()
    await state.reset_data()
