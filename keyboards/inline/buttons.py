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


COURSES = {
    "Sog'lom ovqtalanish guruhi": "https://bekmuxtorov_uz.t.me",
    "Millionerlar klubi": "https://bekmuxtorov_uz.t.me",
    "Himmat 700+ o'smirlar guruhi (12-17 yosh)": "https://bekmuxtorov_uz.t.me"
}

XOS_GURUH = {
    "Erkak": "https://bekmuxtorov_uz.t.me",
    "Ayol": "https://bekmuxtorov_uz.t.me",
}


def course_button(gender: str) -> InlineKeyboardButton:
    course_buttons = InlineKeyboardMarkup(row_width=1)
    for course, url in COURSES.items():
        button = InlineKeyboardButton(text=course, url=url)
        course_buttons.insert(button)

    button = InlineKeyboardButton(
        text=f"Himmat 700+ xos guruhlari({gender}lar)", url=XOS_GURUH.get(gender))
    course_buttons.insert(button)

    return course_buttons
