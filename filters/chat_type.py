from typing import Union

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


