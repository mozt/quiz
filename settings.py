import datetime
import os
from pathlib import Path

APP_HOST = os.getenv('APP_HOST', '127.0.0.1')
APP_PORT = os.getenv('APP_PORT', 8080)
DEBUG = False
PERMANENT_SESSION_LIFETIME = datetime.timedelta(minutes=20)
SECRET_KEY = os.urandom(24)
USER_FILE = Path('users.json')
QUIZ_FILE = Path('quiz.json')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
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
        'level': 'DEBUG',
        'handlers': ['wsgi']
    },
}

