from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot toekn
ADMINS = env.list("ADMINS")  # adminlar ro'yxati
IP = env.str("ip")  # Xosting ip manzili

ADMIN_GROUP_ID = env.str("ADMIN_GROUP_ID")
CHANNELS = env.list("CHANNELS")

DB_USER = env.str("DB_USER")
DB_PASS = env.str("DB_PASS")
DB_NAME = env.str("DB_NAME")
DB_HOST = env.str("DB_HOST")

SPREADSHEET_ID = env.str("SPREADSHEET_ID")

FOR_MAN = env.str("FOR_MAN")
FOR_WOMAN = env.str("FOR_WOMAN")
FOR_TEENAGER = env.str("FOR_TEENAGER")
