import logging
from aiogram import Dispatcher
from utils import auxiliary
from utils.autopost import worker
from models import *
from aiogram import Bot

from config import TOKEN
import asyncio
from handlers import (
    group, my_chat_member,
    private, my_chat_member
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    await init()

    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    group.set_bot(bot)
    auxiliary.set_bot(bot)
    private.set_bot(bot)
    # autopost.set_bot(bot)
    asyncio.create_task(worker.worker())

    dp.include_router(my_chat_member.router)
    dp.include_router(group.router)
    dp.include_router(private.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
