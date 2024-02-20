from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_answer import CallbackAnswer


def already_exist(arg) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    msg = 'Указанный канал уже привязан к этому чату, чтобы удалить его, просто кикните оттуда бота'
    builder.row(InlineKeyboardButton(
        text="КАНАЛ", url=f"https://t.me/{arg}")
    )
    return msg, builder.as_markup()


def no_channel(arg) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
        text="КАНАЛ",
        url=f"https://t.me/{arg}")
    )
    msg = 'Кажется не состою в указанном канале. Попробуйте добавить меня снова:'
    return msg, builder.as_markup()


def warning(channels, mention, warnings_count):
    builder = InlineKeyboardBuilder()

    for channel in channels:
        builder.row(InlineKeyboardButton(
            text="ПОДПИСАТЬСЯ",
            url=f"https://t.me/{channel.username}"
        ))
        msg = f"Уважаемый {mention}! Для того чтобы иметь возможность писать в данном чате, подпишитесь на наш канал. Осталось предупреждений: {3-warnings_count}"
        return msg, builder.as_markup()


def edit_post(task_id) -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()
    # keyboard = InlineKeyboardMarkup()
    # keyboard.row(
    #     InlineKeyboardButton(text="Изменить контент", callback_data="edit_content"))
    # keyboard.row(
    #     InlineKeyboardButton(text="Даты", callback_data="dates"),
    #     InlineKeyboardButton(text="Время", callback_data="time"))
    keyboard.row(
        # InlineKeyboardButton(text="Подтвердить", callback_data="confirm"),
        InlineKeyboardButton(
            text="Удалить", callback_data=f"delete/{task_id}")
        # InlineKeyboardButton(text="Назад", callback_data="abort")
    )
    return keyboard.as_markup()


def chats_autopost(chats) -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()
    for name, id in chats:
        keyboard.row(
            InlineKeyboardButton(text=name, callback_data=f'{id}/{name}'))
    keyboard.row(
        InlineKeyboardButton(text="Назад", callback_data="abort"))
    return keyboard.as_markup()


def list_or_add_kb(list_kb) -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text='Добавить пост', callback_data=f'add'))
    if list_kb:
        keyboard.row(
            InlineKeyboardButton(text="Список постов", callback_data="list"))
    return keyboard.as_markup()


def posts_list(task_data) -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()
    rows = []
    for n, id in enumerate(task_data):
        rows.append(
            InlineKeyboardButton(text=str(n+1), callback_data=id))
    keyboard.row(*rows, width=3)
    return keyboard.as_markup()


# def show_back() -> InlineKeyboardBuilder:
#     keyboard = InlineKeyboardBuilder()
#     keyboard.row(
#         InlineKeyboardButton(text='Показать', callback_data='show_post'))
#     keyboard.row(
#         InlineKeyboardButton(text="Назад", callback_data="abort"))
#     return keyboard
