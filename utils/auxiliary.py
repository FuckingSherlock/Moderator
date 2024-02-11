import asyncio
from aiogram.types import Message
from aiogram import Bot
from config import CustomException, ForbiddenAPI, CustomData
from models import (
    Channel, User,
    create_user,
    remove_user,
    create_chat,
    add_user_chat
)
from answers.react_kb import (
    already_exist,
    no_channel,
    warning
)

bot: Bot


def set_bot(bot_instance):
    global bot
    bot = bot_instance


async def delete_message(msg: Message):
    try:
        await asyncio.sleep(180)
        await msg.delete()
    except ForbiddenAPI as e:
        print(f"Ошибка при удалении сообщения: {e}")
        await asyncio.sleep(180)
        await msg.delete()


async def get_username_mention(user):
    if user.username:
        name = user.username
        mention = '@'+name
    else:
        name = user.full_name
        mention = user.mention_html()
    return name, mention


async def customs(msg):
    user = msg.from_user
    chat = msg.chat
    if user.id in [0, 777000, 136817688]:
        raise CustomException(user=user, chat=chat, message='Это бот или tg')
    name, mention = await get_username_mention(user)
    user_chat_data = await register(user, name, chat)
    parse_mode = None if name.startswith('@') else 'HTML'
    return CustomData(*user_chat_data, parse_mode=parse_mode, mention=mention)


async def register(_user, user_name, _chat):
    chat = await create_chat(_chat.id, _chat.username)
    channels = await Channel.filter(chat=chat).all()
    if not (chat.watched or channels):
        raise CustomException(
            message='Чат не отслеживается, не назначены каналы')
    user = await User.filter(id=_user.id).first()
    if not user:
        member = await bot.get_chat_member(_chat.id, _user.id)
        user = await create_user(_user.id, user_name)
        if member.status.name in ['ADMINISTRATOR', 'OWNER', 'CREATOR']:
            user_chat.admin = True
            await user_chat.save()
    need_sub = await populate_need_sub(user, channels)
    user_chat = await add_user_chat(user=user, chat=chat)
    return [user, chat, user_chat, channels, need_sub]


async def populate_need_sub(user, channels):
    channels_to_delete = []
    channels_to_add = []
    user_sub = await user.fetch_related('channels')
    need_sub = channels
    if user_sub:
        need_sub = [
            channel for channel in channels if channel not in user_sub]
    for chn in need_sub:
        member = await bot.get_chat_member(chn.id, user.id)
        if member.status.name in ['MEMBER', 'ADMINISTRATOR', 'CREATOR']:
            channels_to_add.append(chn)
            need_sub.remove(chn)
        else:
            channels_to_delete.append(chn)
    if channels_to_add:
        await user.channels.add(*channels_to_add)
    if channels_to_delete:
        await user.channels.remove(*[channel for channel in channels_to_delete])
    return need_sub


async def user_warning(data, message: Message):
    await bot.delete_message(chat_id=data.chat.id, message_id=message.message_id)
    data.user_chat.warnings += 1
    await data.user_chat.save()
    if data.user_chat.warnings > 3:
        msg = await bot.send_message(
            data.chat.id, f"Пользователь {data.mention} исключен из чата за нарушение правил.",
            parse_mode=data.parse_mode
        )
        await delete_message(msg)
        await remove_user(data.user, data.user_chat)
        await bot.ban_chat_member(chat_id=data.chat.id, user_id=data.user.id)
    else:
        msg, markup = await warning(
            data.need_sub, data.mention, data.user_chat.warnings)
        _msg = await bot.send_message(
            data.chat.id, msg, reply_markup=markup,
            parse_mode=data.parse_mode
        )
        await delete_message(_msg)


async def react(react_type, message: Message, arg=None):
    match react_type:
        case "not_admin":
            msg = 'Ты не админ, чтоб мной помыкать!'
            await delete_message(await message.answer(text=msg))
            raise CustomException(message=msg)
        case "no_args":
            msg = 'Не передан url чата'
            await delete_message(await message.answer(text=msg))
            raise CustomException(message=msg)
        case "already_exist":
            msg, markup = await already_exist(arg)
            await delete_message(
                await message.answer(text=msg, reply_markup=markup))
            raise CustomException(message=msg)
        case "no_channel":
            msg, markup = await no_channel(arg)
            await delete_message(
                await message.answer(text=msg, reply_markup=markup))
            raise CustomException(message=msg, chat=message.chat)
