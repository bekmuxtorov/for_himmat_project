from aiogram import Dispatcher

from loader import dp
from .is_privatechat import IsPrivateChat, IsPrivateChatForCallback


if __name__ == "filters":
    dp.filters_factory.bind(IsPrivateChat)
    dp.filters_factory.bind(IsPrivateChatForCallback)
