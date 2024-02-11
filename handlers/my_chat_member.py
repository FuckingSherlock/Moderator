from aiogram import Router
from aiogram.enums import ChatType
from filters.chat_type import ChatTypeFilter
from aiogram.types import ChatMemberUpdated
from models import (
    create_chat, create_channel,
    remove_channel, remove_chat)


router = Router()


@router.my_chat_member()
async def on_channel_status_change(chat_member: ChatMemberUpdated):
    chat = chat_member.chat
    status = chat_member.new_chat_member.status
    if status in ['left', 'kicked']:
        if chat.type == ChatType.CHANNEL:
            await remove_channel(chat.id)
        else:
            await remove_chat(chat_member.chat.id)
    elif status in ['administrator', 'member']:
        if chat.type == ChatType.CHANNEL:
            await create_channel(chat.id, chat.username)
        else:
            await create_chat(chat.id, chat.username)
