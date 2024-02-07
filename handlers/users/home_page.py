from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, db
from filters.is_privatechat import IsPrivateChatForCallback, IsPrivateChat
from keyboards.default.default_buttons import make_buttons, build_menu_buttons, not_registered_for_menu_buttons


# Echo bot
@dp.callback_query_handler(IsPrivateChatForCallback(), text_contains="home_page", state='*')
async def bot_echo(call: types.CallbackQuery, state: FSMContext = '*'):
    user_id = call.from_user.id
    user = await db.select_user(telegram_id=user_id)
    if not user:
        await call.message.answer("Xush kelibsiz!\n\nBotdan foydalanish uchun quyidagi tugma yordamida ro'yhatdan o'ting!", reply_markup=make_buttons(["Ro'yhatdan o'tish"]))
    else:
        await call.message.answer("🏠 Bosh sahifa", reply_markup=build_menu_buttons)
    await state.finish()
    await state.reset_data()


@dp.message_handler(IsPrivateChat(), text="🏠 Bosh sahifa", state='*')
async def bot_echo(message: types.Message, state: FSMContext = '*'):
    user_id = message.from_user.id
    user = await db.select_user(telegram_id=user_id)
    if not user:
        await message.answer("✅ Xush kelibsiz!\n\n", reply_markup=not_registered_for_menu_buttons)
    else:
        await message.answer("🏠 Bosh sahifa", reply_markup=build_menu_buttons)
    await state.finish()
    await state.reset_data()
