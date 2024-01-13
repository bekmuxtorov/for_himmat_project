from aiogram import types
from loader import dp

from filters.is_privatechat import IsPrivateChat

# Echo bot
@dp.message_handler(IsPrivateChat(), state=None)
async def bot_echo(message: types.Message):
    await message.answer("🛠️ Aniqlanmagan buyruq!")
