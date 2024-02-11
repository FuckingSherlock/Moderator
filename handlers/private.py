from aiogram import Router

from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Bot
from config import CustomException, ForbiddenAPI
from models import *

from aiogram.filters.command import Command, CommandObject
from aiogram.exceptions import TelegramForbiddenError
from filters.chat_type import ChatTypeFilter

from utils.auxiliary import *

bot: Bot


def set_bot(bot_instance):
    global bot
    bot = bot_instance


router = Router()
router.message.filter(
    ChatTypeFilter(chat_type=["private"]),
    # ContentTypeFilter(content_type=[])
)

        
# @router.message(Command("create"))
@router.message()
async def process_message(message: Message):
    print(message.content_type.__dict__)
    print(message.text)
    print(message.__dict__)
    #     try:
    #         data = await customs(message)
    #         if data.user_chat.admin:
    #             return
    #         if not data.need_sub:
    #             raise Exception
    #         await user_warning(data, message)
    #     except CustomException as e:
    #         print(e)


# # @router.message(Command("list"))
# @router.message(Command("create"))
# async def command(message: Message, command: CommandObject):
#     try:
#         chat = await Chat.filter(id=message.chat.id).first()
#         member = await bot.get_chat_member(chat.id, message.from_user.id)
#         if member.status.name not in ['ADMINISTRATOR', 'CREATOR']:
#             await react('not_admin', message)
#         if not command.args:
#             await react('no_args', message)
#         channel_name = command.args.split(' ')[-1].split('/')[-1]
#         channel = await Channel.filter(username=channel_name).prefetch_related('chat').first()
#         try:
#             if not channel:
#                 raise ForbiddenAPI
#             if channel.chat == chat:
#                 await react('already_exist', message, arg=channel.username)
#             await bot.get_chat_member(channel.id, bot.id)
#             chat.watched, channel.chat = True, chat
#             await chat.save()
#             await channel.save()
#             _msg = await message.answer('Чат успешно призязан')
#             await delete_message(_msg)
#         except (TelegramForbiddenError, ForbiddenAPI):
#             await react('no_channel', message, channel_name)
#     except (CustomException, ForbiddenAPI) as e:
#         print(e)
