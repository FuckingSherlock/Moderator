from typing import Union
from datetime import datetime
from aiogram.filters import Filter
from aiogram.types import Message


class ChatTypeFilter(Filter):
    def __init__(self, chat_type: Union[str, list]):
        self.chat_type = chat_type

    async def __call__(self, message: Message) -> bool:
        if isinstance(self.chat_type, str):
            return message.chat.type == self.chat_type
        else:
            return message.chat.type in self.chat_type


class ContentTypeFilter(Filter):
    def __init__(self, content_type: list):
        self.content_type = content_type

    async def __call__(self, message: Message) -> bool:
        return message.content_type not in self.content_type


class DateTimeFilter(Filter):
    def __init__(self, date_time_type: str):
        self.date_time = date_time_type

    async def __call__(self, message: Message) -> Union[bool, list, dict]:
        dates = {}
        times = []
        msg = message.text
        if self.date_time == 'time':
            try:
                lst = msg.split(', ') if ',' in msg else [msg]
                for i in lst:
                    times.append(datetime.strptime(i, '%H:%M').time())
                return {"date_time_data": times}
            except ValueError as e:
                return False
        elif self.date_time == 'date':
            try:
                date = msg.split(' - ')
                current_date = datetime.now().date()
                dates['start'] = datetime.strptime(
                    date[0], "%d.%m").replace(year=current_date.year).date()
                dates['end'] = datetime.strptime(date[1], "%d.%m").replace(
                    year=current_date.year).date()

                if dates['end'] < dates['start']:
                    dates['end'] = dates['end'].replace(year=current_date.year + 1)

                return {"date_time_data": dates}
            except ValueError:
                return False
