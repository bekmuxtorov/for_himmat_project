from aiogram import types
from loader import dp, db

from filters.is_privatechat import IsPrivateChat
from keyboards.default.default_buttons import make_buttons

# Echo bot


@dp.message_handler(IsPrivateChat(), state=None)
async def bot_echo(message: types.Message):
    if await db.select_user(telegram_id=message.from_user.id):
        await message.answer("🛠️ Aniqlanmagan buyruq!")
    else:
        await message.answer("Xush kelibsiz!\n\nBotdan foydalanish uchun quyidagi tugma yordamida ro'yhatdan o'ting!", reply_markup=make_buttons(["Ro'yhatdan o'tish"]))
