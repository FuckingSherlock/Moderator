from collections import namedtuple
import sys
import environs


env = environs.Env()
env.read_env('.env')


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


TORTOISE_ORM = {
    "connections": {
        "default": env('DATABASE_CONNECTION_URL')
    },
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default",
        }
    },
    "aerich": {
        "migration_store": "aerich.models.AerichMigrationStore",
    },
}

TOKEN = env('BOT_TOKEN')


# 3tcoGZH5sN40f1R
# tmux attach-session -t 0
#  aerich init -t config.TORTOISE_ORM
