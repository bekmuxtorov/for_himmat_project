from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import bot

from data.config import FOR_MAN, FOR_WOMAN, FOR_TEENAGER


def become_member_buttons(must_member: dict):
    become_member = InlineKeyboardMarkup(row_width=1)
    for channel, title in must_member.items():
        channel_link = f'https://{channel}.t.me'
        button = InlineKeyboardButton(text=title, url=f"{channel_link}")
        become_member.insert(button)

    check_button = InlineKeyboardButton(
        text='🔔 Obuna bo\'ldim', callback_data="check_button")
    become_member.insert(check_button)
    return become_member


COURSES = {
    "Sog'lom ovqtalanish guruhi": "https://t.me/togriovqatlanishklub",
    # "Millionerlar klubi": "https://t.me/millionerlar_klubi_kutish_guruhi",
    # "Himmat 700+ o'smirlar guruhi (12-17 yosh)": "https://bekmuxtorov_uz.t.me"
}

SPECIAL_GROUPS = {
    "Erkaklar 👳": FOR_MAN,
    "O'smir o'g'il bolalar🙋": FOR_TEENAGER,
    "Ayollar🧕": FOR_WOMAN
}


def course_button(gender: str) -> InlineKeyboardButton:
    course_buttons = InlineKeyboardMarkup(row_width=1)
    for course, url in COURSES.items():
        button = InlineKeyboardButton(text=course, url=url)
        course_buttons.insert(button)
    button = InlineKeyboardButton(
        text="Millionerlar klubi", callback_data="million_course")
    course_buttons.insert(button)

    for title, link in SPECIAL_GROUPS.items():
        button = InlineKeyboardButton(
            text=f"Himmat 700+ xos guruhlari({title})", url=link)
        course_buttons.insert(button)

    button = InlineKeyboardButton(
        text="🏠 Bosh sahifa", callback_data="home_page")
    course_buttons.insert(button)
    return course_buttons


confirmation_button = InlineKeyboardMarkup(row_width=2)
confirmation_button.insert(InlineKeyboardButton(
    callback_data="yes_send", text="Ha, jo'natilsin."))
confirmation_button.insert(InlineKeyboardButton(
    callback_data="no_send", text="Yo'q, bekor qilinsin."))


def talk_buttons(titles: dict) -> InlineKeyboardMarkup:
    talk_buttons = InlineKeyboardMarkup(row_width=1)
    for id, title in titles.items():
        button = InlineKeyboardButton(text=title, callback_data=f"talk_{id}")
        talk_buttons.insert(button)
    return talk_buttons


async def reply_buttons(question_id) -> InlineKeyboardMarkup:
    reply_button = InlineKeyboardMarkup(row_width=1)
    from aiogram.utils.deep_linking import get_start_link

    link = await get_start_link(f"reply_question:{question_id}", encode=True)
    button = InlineKeyboardButton(
        text="Javob qaytarish", url=link)
    reply_button.insert(button)
    return reply_button
