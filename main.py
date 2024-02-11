import logging
from aiogram import Dispatcher
from utils import auxiliary
from models import *
from aiogram import Bot
from config import TOKEN
import asyncio
from handlers import group, my_chat_member, private


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    await init()

    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    group.set_bot(bot)
    auxiliary.set_bot(bot)

    dp.include_router(my_chat_member.router)
    dp.include_router(group.router)
    dp.include_router(private.router)

    # dp.include_routers(different_types.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
