from tortoise import Tortoise, fields, models
from config import TORTOISE_ORM


class Chat(models.Model):
    id = fields.BigIntField(pk=True)
    username = fields.CharField(max_length=255)
    watched = fields.BooleanField(default=False)
    user_chats = fields.ReverseRelation["UserChat"]
    channels = fields.ReverseRelation["Channel"]


class Channel(models.Model):
    id = fields.BigIntField(pk=True)
    username = fields.CharField(max_length=255)
    chat = fields.ForeignKeyField(
        "models.Chat", related_name="chat", null=True)


class User(models.Model):
    id = fields.BigIntField(pk=True)
    username = fields.CharField(max_length=255)
    channels = fields.ManyToManyField(
        "models.Channel", related_name="channels", reverse="users")
    user_chats = fields.ReverseRelation["UserChat"]


class UserChat(models.Model):
    user = fields.ForeignKeyField("models.User", related_name="user_chats")
    chat = fields.ForeignKeyField("models.Chat", related_name="user_chats")
    warnings = fields.IntField(default=0)
    admin = fields.BooleanField(default=False)


async def add_user_chat(user, chat):
    user_chat = await UserChat.filter(chat=chat, user=user).first()
    if not user_chat:
        user_chat = await UserChat.create(user=user, chat=chat)
    return user_chat


async def create_chat(chat_id, username):
    chat = await Chat.filter(id=chat_id).first()
    if not chat:
        chat = await Chat.create(id=chat_id, username=username)
        print("Чат успешно создан.")
    return chat


async def create_user(user_id, username):
    user = await User.filter(id=user_id).first()
    if not user:
        user = await User.create(id=user_id, username=username)
        print("Пользователь успешно создан.")
    return user


async def create_channel(id, channel_username):
    channel = await Channel.filter(id=id).first()
    if not channel:
        channel = await Channel.create(id=id, username=channel_username)
        print("Канал успешно создан.")
    return channel


async def remove_user(user, user_chat):
    await user.channels.clear()
    await user_chat.delete()
    await user.delete()


async def remove_chat(chat_id):
    chat = await Chat.filter(id=chat_id).first()
    if chat:
        try:
            await UserChat.filter(chat=chat).delete()
        except:
            pass
        try:
            await Channel.filter(chat=chat).update(chat=None)
        except:
            pass
        await chat.delete()
        print('Чат удален')


async def remove_channel(channel_id):
    channel = await Channel.filter(id=channel_id).prefetch_related('chat').first()
    if channel:
        if channel.chat:
            if not await Channel.filter(chat=channel.chat).all():
                channel.chat.watched = False
                await channel.chat.save()
        await channel.delete()
        print('Канал удален')


async def init():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()



