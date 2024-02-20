from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.filters.state import StatesGroup, State
from aiogram import Bot
from models import *
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from utils.auxiliary import *
from answers.react_kb import (
    edit_post, chats_autopost,
    list_or_add_kb, posts_list)
from filters.filters import DateTimeFilter
import datetime
from utils.auxiliary import form_description, get_user_chats
from utils.autopost import worker

bot: Bot


def set_bot(bot_instance):
    global bot
    bot = bot_instance


router = Router()


class PostStates(StatesGroup):
    chat = State()
    list = State()
    content = State()
    date = State()
    time = State()
    confirm = State()
    demo = State()


@router.message(Command('select_chat'))
async def create_post(message: Message, state: FSMContext):
    await state.clear()
    # set_message(message)
    user_chats = await get_user_chats(message)
    chats_names = []
    if user_chats:
        for user_chat in user_chats:
            chats_names.append((user_chat.chat.username, user_chat.chat.id))
        await message.answer(
            'Выберите чат:',
            reply_markup=chats_autopost(chats_names))
        await state.set_state(PostStates.chat)
    else:
        await message.answer('Пшол нахуй, ноунейм несчатсный')


@router.callback_query(PostStates.chat)
async def handle_callback_query(callback_query: CallbackQuery, state: FSMContext):
    chat_id = int(callback_query.data.split('/')[0])
    chat = await Chat.filter(id=chat_id).first()
    posts = await worker.get_queue()
    list_kb = None
    list_kb = any(task['chat_id'] == chat_id for task in posts.values())
    await state.update_data(chat=chat)
    await callback_query.message.answer(text=chat.username, reply_markup=list_or_add_kb(list_kb))
    await state.set_state(PostStates.list)


@router.callback_query(PostStates.list)
async def state_list_or_add(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == 'add':
        await callback_query.message.answer('Отправьте сообщение для автопоста')
        await state.set_state(PostStates.content)
    elif callback_query.data == 'list':
        posts = await worker.get_queue()
        await state.update_data(list=posts)
        text = ''
        for n, post in enumerate(posts.values()):
            text += f'\n{n+1}. {post["message"].text[:45]}'
        await callback_query.message.answer(
            text=f'Список постов: {text}',
            reply_markup=posts_list(posts.keys()))
        await state.set_state(PostStates.demo)


@router.callback_query(PostStates.demo)
async def post_demo(callback_query: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    post_id = callback_query.data
    posts = await worker.get_queue()
    data = None
    for task_id, post in posts.items():
        if task_id == post_id:
            data = post
            break
    await callback_query.message.answer(data.get('descr'))
    await data.get('message').send_copy(
        chat_id=data['message'].from_user.id,
        reply_markup=edit_post(post_id))
    await state.set_state(PostStates.confirm)


@router.callback_query(PostStates.confirm)
async def confirm(callback_query: CallbackQuery, state: FSMContext):
    task_id = callback_query.data.split('/')[1]
    await worker.remove_from_queue(task_id)
    await callback_query.message.answer('Пост удален из очереди')
    # await state.set_state(PostStates.list)
    await state.clear()


@router.message(PostStates.content)
async def process_content(message: Message, state: FSMContext):
    await state.update_data(content=message)
    await message.reply('Отлично! Теперь отправьте дату начала и окончания в формате: "ДД.ММ - ДД.ММ"')
    await state.set_state(PostStates.date)


@router.message(PostStates.date, DateTimeFilter('date'))
async def process_content(message: Message, state: FSMContext, date_time_data: datetime):
    await state.update_data(date=date_time_data)
    await message.reply('Отлично! Теперь отправьте временные точки постинга в формате: "ЧЧ:ММ" или "ЧЧ:ММ, ЧЧ:ММ,..."')
    await state.set_state(PostStates.time)


@router.message(PostStates.time, DateTimeFilter('time'))
async def process_content(message: Message, state: FSMContext, date_time_data: datetime):
    await state.update_data(time=date_time_data)
    data = await form_description(await state.get_data())
    task_id = await worker.add_to_queue(data)

    await message.answer('Пост создан')
    await message.answer(data.get('descr'))
    await data.get('message').send_copy(
        chat_id=message.from_user.id,
        reply_markup=edit_post(task_id))
    # await message.send_copy(chat_id=data.get('chat_id'))
    # await state.set_state(PostStates.demo)


# @router.callback_query(F.data == 'show_post')
# async def process_content(callback_query: CallbackQuery, state: FSMContext):
#     data = await form_description(await state.get_data())
#     message = data.get('message')
#     chat = data.get('chat')
#     await bot.send_message(chat_id=chat.id, text=data.get('text'))
#     await message.send_copy(chat_id=callback_query.from_user.id, reply_markup=edit_post(task_id))
#     await state.set_state(PostStates.confirm)


# @router.message(Command('abort'))
# async def create_post(message: Message, state: FSMContext):
#     await state.clear()
#     await message.reply('Возврат в главное меню')
#     await state.clear()
# @router.callback_query(PostStates.confirm)
# async def handle_callback_query(callback_query: CallbackQuery, state: FSMContext):
#     cb = callback_query.data
#     match callback_query.data:
#         case 'edit_content':
#             await state.set_state(PostStates.content)
#             await callback_query.answer('Отправьте новое сообщение')
#         case 'dates':
#             await state.set_state(PostStates.confirm)
#         case 'time':
#             await state.set_state(PostStates.confirm)
#         case 'confirm':
#             await state.set_state(PostStates.confirm)
#         case 'abort':
#             await state.set_state(PostStates.confirm)


# F.text.is_('confirm')
# storage = MemoryStorage()

# @router.message()
# async def process_message(message: Message):
#     # print(message.message_id)
#     # print(message.chat.id)
#     user = await User.get_or_none(id=message.from_user.id)
#     if not user:
#         raise CustomException
#     # print(user.id)
#     # user_chats_admin = await UserChat.filter(user=user, admin=True).select_related('chat')
#     # chats = [user_chat.chat for user_chat in user_chats_admin]
#     # msg = await bot.edit_message_text(text=f'{randint(1,100)} TEST')
#     # msg = await msg.send_copy(chat_id=-1002083023561)
#     # msg = await message.send_copy(chat_id=user.id)

#     # print(msg.message_id)
#     # async with aiohttp.ClientSession() as session:
#     #     url = f'https://api.telegram.org/bot{TOKEN}/getMessages?chat_id=-1002083023561&message_id=1126'
#     #     async with session.post(url) as response:
#     #         result = await response.json()
#     #         print(result)
#     #         return result
