from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def make_buttons(words: list, row_width: int = 1) -> ReplyKeyboardMarkup:
    buttons_group = ReplyKeyboardMarkup(
        row_width=row_width, resize_keyboard=True)
    for word in words:
        if word is not None:
            buttons_group.insert(KeyboardButton(text=word))
    return buttons_group


contact_request_button = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(
                text="Telefon raqamni ulashish",
                request_contact=True
            )
        ],
    ]
)


def build_talk_buttons(titles: dict) -> ReplyKeyboardMarkup:
    talk_buttons = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for idx, title in titles.items():
        button = KeyboardButton(text=title)
        talk_buttons.insert(button)
    button = KeyboardButton(text="🏠 Bosh sahifa")
    talk_buttons.insert(button)
    return talk_buttons


build_menu_buttons = make_buttons(["📚 Barcha suxbatlar(Himmat 700+) 📚", "📝 Ustozga savol yo'llash 📝",
                                  "📍(Himmat 700+ loyihalari havolasini olish)📍", "Taklif va e'tirozlar✍️", "Himmat 700+ Ijtimoiy tarmoqdagi havolalar💻🔆"], row_width=1)
