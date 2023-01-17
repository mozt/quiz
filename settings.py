import datetime
import os
from pathlib import Path
from base64 import b64encode
from multiprocessing import Array

APP_HOST = os.getenv('APP_HOST', '127.0.0.1')
APP_PORT = os.getenv('APP_PORT', 8080)
DEBUG = False
PERMANENT_SESSION_LIFETIME = datetime.timedelta(minutes=20)
# SECRET_KEY = os.urandom(24)
# SECRET_KEY = os.getenv('SECRET_KEY')
try:
    with open('.secret.key', 'rt') as f:
        SECRET_KEY = f.read()
        f.close()
except FileNotFoundError:
    SECRET_KEY = b64encode(os.urandom(48)).decode('UTF8')
    with open('.secret.key', 'wt') as f:
        f.write(SECRET_KEY)
        f.close()

# if os.getenv('SECRET_KEY') is None:
#     SECRET_KEY = b64encode(os.urandom(48)).decode('UTF8')
#     os.environ['SECRET_KEY'] = SECRET_KEY
# else:
#     SECRET_KEY = os.getenv('SECRET_KEY')

# # SECRET_KEY = Value('c', os.urandom(48))
# _secret_array = Array('i', os.urandom(48))
# # SECRET_KEY = bytearray()
# # for i in _secret_array:
# #     print(i)
# #     SECRET_KEY.extend(i)
# SECRET_KEY = b64encode(bytes([_secret_array[_] for _ in range(len(_secret_array))])).decode('UTF8')
# print(SECRET_KEY)

USER_FILE = Path('users.json')
QUIZ_FILE = Path('quiz.json')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }
    },
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    },
}

