from aiogram import Router
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


@router.message(PostStates.content)
async def process_content(message: Message, state: FSMContext):
    await state.update_data(content=message)
    await message.reply('Отлично! Теперь отправьте дату начала и окончания в формате: "ДД.ММ - ДД.ММ"')
    await state.set_state(PostStates.date)


@router.message(Command('select_chat'))
async def create_post(message: Message, state: FSMContext):
    await state.clear()
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
            text += f'\n{n+1}. {post["message"].html_text[:45]}'
        await callback_query.message.answer(
            text=f'Список постов: {text}',
            reply_markup=posts_list(posts.keys()))
        await state.set_state(PostStates.demo)


@router.callback_query(PostStates.demo)
async def post_demo(callback_query: CallbackQuery, state: FSMContext):
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
    await state.clear()


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
