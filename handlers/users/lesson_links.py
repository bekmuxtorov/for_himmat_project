from aiogram import types
from loader import dp, db

from filters.is_privatechat import IsPrivateChat
from keyboards.inline.buttons import course_button


@dp.message_handler(IsPrivateChat(), text="📍(Himmat 700+ loyihalari havolasini olish)📍")
async def bot_echo(message: types.Message):
    user = await db.select_user(telegram_id=message.from_user.id)
    gender = user.get("gender")
    await message.answer("Quyidagi guruhlarga qo'shilishingiz mumkin 😊", reply_markup=course_button(gender))
