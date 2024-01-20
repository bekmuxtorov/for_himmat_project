from aiogram import types
from loader import dp

from filters.is_privatechat import IsPrivateChat


@dp.message_handler(IsPrivateChat(), text="Suhbatlar")
async def bot_echo(message: types.Message):
    await message.answer("🛠️ Ishlar olib borilmoqda...")
