from aiogram import types
from loader import dp

from filters.is_privatechat import IsPrivateChat


@dp.message_handler(IsPrivateChat(), text="Himmat 700+ Ijtimoiy tarmoqdagi havolalar💻🔆")
async def bot_echo(message: types.Message):
    text = "<b>💡 Ijrimoiy tarmoqlardagi manzillarimiz:</b>\n\n"
    text += "1. Telegram: <a href='https://t.me/Zufar_Domla'>@Zufar_Domla</a>"
    text += "\n\n2. Facebook: <a href='https://www.facebook.com/zufardomlashosalimov?mibextid=LQQJ4d'>@zufardomlashosalimov</a>"
    text += "\n\n3. Instagram: <a href='https://www.instagram.com/zufarjon_shosalimov?igsh=MWx6cWZiemgyeXEzMA%3D%3D&utm_source=qr'>@zufarjon_shosalimov</a>"
    text += "\n\n4. YouTube: <a href='https://youtube.com/@Zufar_domla'>@Zufar_domla</a>"
    text += "\n\n5. Umma life: <a href='https://ummalife.com/zufardomlashasalimov'>@zufardomlashasalimov</a>"
    await message.answer(text=text)
