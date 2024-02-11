from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


async def already_exist(arg) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    msg = 'Указанный канал уже привязан к этому чату, чтобы удалить его, просто кикните оттуда бота'
    builder.row(InlineKeyboardButton(
        text="КАНАЛ", url=f"https://t.me/{arg}")
    )
    return msg, builder.as_markup()


async def no_channel(arg) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
        text="КАНАЛ",
        url=f"https://t.me/{arg}")
    )
    msg = 'Кажется не состою в указанном канале. Попробуйте добавить меня снова:'
    return msg, builder.as_markup()


async def warning(channels, mention, warnings_count):
    builder = InlineKeyboardBuilder()

    for channel in channels:
        builder.row(InlineKeyboardButton(
            text="ПОДПИСАТЬСЯ",
            url=f"https://t.me/{channel.username}"
        ))
        msg = f"Уважаемый {mention}! Для того чтобы иметь возможность писать в данном чате, подпишитесь на наш канал. Осталось предупреждений: {3-warnings_count}",
        return msg, builder.as_markup()
