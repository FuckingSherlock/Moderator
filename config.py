from collections import namedtuple
import sys

TOKEN = '6730054093:AAHBUqAx1lL_61FpzKwQHtt9AHN1Fg27JZo'


class ForbiddenAPI(Exception):
    pass


class CustomException(BaseException):
    def __init__(self, user=None, chat=None, message='EXCEPTION'):
        self.user = user
        self.chat = chat
        self.message = message
        frame = sys._getframe(1)
        self.call_location = (frame.f_code.co_filename, frame.f_lineno)
        super().__init__(message)

    def __str__(self):
        # \nCтрокa: {self.call_location[1]}."
        return f"Ошибка: {self.message}."


CustomData = namedtuple(
    'CustomData', [
        'user', 'chat', 'user_chat',
        'channels', 'need_sub',
        'parse_mode', 'mention'
    ]
)


# 3tcoGZH5sN40f1R
# tmux attach-session -t 0
