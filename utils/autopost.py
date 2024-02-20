from aiogram.types import Message
from aiogram import Bot
from models import *
from aiogram.filters.command import Command
from utils.auxiliary import *
import datetime
from datetime import datetime, timedelta


class AutopostWorker:
    def __init__(self):
        self.autopost_queue = asyncio.Queue()
        self.to_remove = []
        self.posts_dict = {}

    async def worker(self):
        print('start worker')
        while True:
            # await asyncio.sleep(10)
            await asyncio.sleep(60)
            current_datetime = datetime.now()
            queue_length = self.autopost_queue.qsize()
            for _ in range(queue_length):
                task_data = await self.autopost_queue.get()
                if task_data['id'] in self.to_remove:
                    self.to_remove.remove(task_data['id'])
                    del self.posts_dict[task_data['id']]
                    self.autopost_queue.task_done()
                    print('POST REMOVED')
                    continue
                if task_data['date']['start'] <= current_datetime.date() <= task_data['date']['end']:
                    for post_time in task_data['times']:
                        post_datetime = datetime.combine(
                            current_datetime.date(), post_time)
                        mintime = current_datetime - timedelta(minutes=1)
                        maxtime = current_datetime + timedelta(minutes=1)
                        if mintime <= post_datetime <= maxtime:
                            await self.post_message(task_data['message'], task_data['chat'].id)
                await self.autopost_queue.put(task_data)

    async def add_to_queue(self, post_data):
        task_id = str(hash(str(post_data)))
        await self.autopost_queue.put({'id': task_id, **post_data})
        self.posts_dict[task_id] = post_data
        print('POST ADDED')
        return task_id

    async def get_queue(self):
        return self.posts_dict

    async def remove_from_queue(self, task_id):
        self.to_remove.append(task_id)

    async def post_message(self, message: Message, chat_id):
        print('POST SENDED')
        await message.send_copy(chat_id=chat_id)


worker = AutopostWorker()
