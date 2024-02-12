from aiogram import types
from typing import Union


async def build_message_group(message: Union[types.CallbackQuery, types.Message], user, question_text):
    is_registered = False
    if isinstance(message, types.CallbackQuery):
        username = message.message.from_user.username
        telegram_id = message.message.from_user.id
        full_name = message.message.from_user.full_name

    elif isinstance(message, types.Message):
        username = message.from_user.username
        telegram_id = message.from_user.id
        full_name = message.from_user.full_name

    if user:
        is_registered = True
        full_name = user.get("full_name")
        phone_number = user.get("phone_number")
        age = user.get("age")
        gender = user.get("gender")
        if username:
            send_text = f"📝 Ustozga savol yo'llandi.\n\n<b>Kimdan:</b> {full_name}\n<b>Telegam username:</b> @{username}\n<b>Yosh:</b> {age} yosh\n<b>Jins:</b> {gender}\n<b>Telefon raqam:</b> {phone_number}\n\n<i>{question_text}</i>"
        else:
            send_text = f"📝 Ustozga savol yo'llandi.\n\n<b>Kimdan:</b> {full_name}\n<b>Telegam ID:</b> {telegram_id}\n<b>Yosh:</b> {age} yosh\n<b>Jins:</b> {gender}\n<b>Telefon raqam:</b> {phone_number}\n\n<i>{question_text}</i>"

    else:
        if username:
            send_text = f"📝 Ustozga savol yo'llandi.\n\n<b>Kimdan:</b> {full_name}\n<b>Telegam username:</b> @{username}\n\n<i>{question_text}</i>"
        else:
            send_text = f"📝 Ustozga savol yo'llandi.\n\n<b>Kimdan:</b> {full_name}\n<b>Telegam ID:</b> {telegram_id}\n\n<i>{question_text}</i>"

    return is_registered, send_text
