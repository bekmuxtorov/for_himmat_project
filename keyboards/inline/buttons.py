from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import bot


def become_member_buttons(must_member: dict):
    become_member = InlineKeyboardMarkup(row_width=1)
    for channel, title in must_member.items():
        button = InlineKeyboardButton(text=title, url=f"{channel}")
        become_member.insert(button)

    check_button = InlineKeyboardButton(
        text='🔔 Obuna bo\'ldim', callback_data="check_button")
    become_member.insert(check_button)
    return become_member
