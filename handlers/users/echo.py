from aiogram import types
from loader import dp, db

from filters.is_privatechat import IsPrivateChat
from keyboards.default.default_buttons import make_buttons, not_registered_for_menu_buttons

# Echo bot


@dp.message_handler(IsPrivateChat(), state=None)
async def bot_echo(message: types.Message):
    if await db.select_user(telegram_id=message.from_user.id):
        await message.answer("🛠️ Aniqlanmagan buyruq!")
    else:
        await message.answer("✅ Xush kelibsiz!\n\n", reply_markup=not_registered_for_menu_buttons)
