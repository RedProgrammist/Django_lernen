# settings.py
import os

from django.conf.global_settings import ALLOWED_HOSTS
from environ import Env
from pathlib import Path
import ast

BASE_DIR = Path(__file__).resolve().parent.parent
env = Env()
Env.read_env(BASE_DIR / '.env')


SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
# ALLOWED_HOSTS = ['localhost', '127.0.0.1']
Use_MySQL = env('USE_MYSQL')



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',
    'rest_framework',
    'rest_framework.authtoken',
]


if Use_MySQL:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': env('DB_NAME'),
            'USER': env('DB_USER'),
            'PASSWORD': env('DB_PASS'),
            'HOST': env('DB_HOST'),
            'PORT': env('DB_PORT', default='3306'),
        }
    }
else:
    DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
     }
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # можешь указать путь к своим шаблонам, если хочешь
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
STATIC_URL = '/static/'

BASE_DIR = Path(__file__).resolve().parent.parent

# Главный URL конфиг проекта
ROOT_URLCONF = 'myproject.urls'


# Настройка WSGI (точка входа для веб-сервера)
WSGI_APPLICATION = 'myproject.wsgi.application'

# Настройки базы данных (по умолчанию SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Пароли: базовые проверки безопасности
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'myapp.pagination.MyCursorPagination',
    'DEFAULT_AUTHENTICATION_CLASSES': [
                                  'rest_framework_simplejwt.authentication.JWTAuthentication',],

}
from datetime import timedelta
SIMPLE_JWT = {
 'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
 'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}
# Локализация
LANGUAGE_CODE = 'ru-ru'  # или 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True
USE_L10N = True
USE_TZ = True

# Статика (css, js, картинки)

STATICFILES_DIRS = [BASE_DIR / "static"]  # если есть папка static

# Медиа (если нужно загружать файлы)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)  # создаём папку logs, если её нет

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {name} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname}: {message}',
            'style': '{',
        },
    },

    'handlers': {
        # 1) Вывод в консоль
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'simple',
        },
        # 2) HTTP-запросы → logs/http_logs.log
        'http_file': {
            'class': 'logging.FileHandler',
            'level': 'INFO',
            'formatter': 'verbose',
            'filename': os.path.join(LOG_DIR, 'http_logs.log'),
        },
        # 3) SQL-запросы → logs/db_logs.log
        'db_file': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'verbose',
            'filename': os.path.join(LOG_DIR, 'db_logs.log'),
        },
    },

    'loggers': {
        # Логи работы сервера (runserver)
        'django.server': {
            'handlers': ['console', 'http_file'],
            'level': 'INFO',
            'propagate': False,
        },
        # Логи SQL-запросов
        'django.db.backends': {
            'handlers': ['db_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}
