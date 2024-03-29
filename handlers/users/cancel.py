from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, db, bot
from keyboards.default.default_buttons import make_buttons, build_menu_buttons, not_registered_for_menu_buttons
from states.register import Register


# Echo bot
@dp.message_handler(text="❌ Bekor qilish", state='*')
async def bot_echo(message: types.Message, state: FSMContext = '*'):
    user_id = message.from_user.id
    user = await db.select_user(telegram_id=user_id)
    if message.chat.type == types.ChatType.PRIVATE:
        if not user:
            state_name = await state.get_state()
            if state_name in Register.all_states_names:
                await message.answer("❌ Jarayon bekor qilindi.\n\nQayta urinish uchun quyidagi tugmani ezing!", reply_markup=make_buttons(["Ro'yhatdan o'tish"]))
            else:
                await message.answer("❌ Jarayon bekor qilindi.", reply_markup=not_registered_for_menu_buttons)
        else:
            await message.answer("❌ Jarayon bekor qilindi.", reply_markup=build_menu_buttons)
    else:
        msg = await bot.send_message(chat_id=message.chat.id,
                                     text="O'chirish uchun jo'natilgan xabar!",
                                     reply_markup=types.ReplyKeyboardRemove(),
                                     )
        await bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
    await state.finish()
    await state.reset_data()
