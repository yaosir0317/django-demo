"""
Django settings for django_demo project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'obxgbv@mdpl-#=i)%7m&k2t$51nz=7x6o17ryblq&0ew21sixp'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api.apps.ApiConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "api_tools.my_middleware.MyMiddleware"
]

ROOT_URLCONF = 'django_demo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'django_demo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'  # 更改时区

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "/static/")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]


# exception mail  报警邮件的配置信息
EXCEPTION_MAIL_FROM = 'xx@163.com'
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = '587'
EMAIL_HOST_USER = 'xx@163.com'
EMAIL_HOST_PASSWORD = 'xxxxxxx'
EMAIL_USE_SSL = True
EXCEPTION_MAIL_LIST = ["ss@163.com"]  # 接受报警邮件的列表
FEI_SHU_URL = ""  # 飞书群机器人报警url

# logs
FORMATTERS = {
    'access': {
        'format': '%(asctime)s %(client_ip)s %(x_forwarded_ip)s %(process)d/%(thread)d %(http_user_agent)s '
                  '%(server_name)s %(protocol)s %(path)s %(status)s %(content_length)s %(duration)s '
                  '%(levelname)s %(message)s',
        'datefmt': "%Y-%m-%d %H:%M:%S"
    },
    'default': {
        'format': '%(asctime)s%(process)d/%(thread)d%(name)s%(funcName)s %(lineno)s%(levelname)s%(message)s',
        'datefmt': "%Y-%m-%d %H:%M:%S"
    }
}

HANDLERS = {
    'mail_handler': {
        'level': 'ERROR',
        'class': 'api_tools.my_handler.SendEmailHandler'
    },
    'feishu_handler': {
        'level': 'ERROR',
        'class': 'api_tools.my_handler.SendFeiShuHandler'
    },
    'access': {
        'level': 'INFO',
        'class': 'logging.handlers.TimedRotatingFileHandler',
        'filename': 'access.log',
        'when': 'midnight',
        'interval': 1,
        'formatter': 'access'
    },
    'celery': {
        'level': 'INFO',
        'class': 'logging.StreamHandler',
        'formatter': 'default'
    },
    'default': {
        'level': 'INFO',
        'class': 'logging.handlers.TimedRotatingFileHandler',
        'filename': 'default.log',
        'when': 'midnight',
        'interval': 1,
        'formatter': 'default'
    },
    'console': {
        'class': 'logging.StreamHandler',
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': FORMATTERS,
    'handlers': HANDLERS,
    'loggers': {
        'django': {
            'handlers': ['default', 'console'],
            'level': 'INFO',
            'propagate': False
        },
        'access': {
            'handlers': ['access'],
            'level': 'INFO',
            'propagate': False
        },
        'celery': {
            'handlers': ['celery', 'console'],
            'level': 'INFO',
            'propagate': False
        }
    },
    'root': {
        'handlers': ['default', 'console'],
        'level': 'DEBUG'
    },
}
