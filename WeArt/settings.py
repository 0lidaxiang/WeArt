"""
Django settings for WeArt project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import socket

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0(5p$h=5c3fve1n$b9j!#fuhif7a4-2jn#^ze(=jt%bz^(+q%r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '192.168.122.248', '192.168.122.43']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'WeArt.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR + "/templates",],
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

WSGI_APPLICATION = 'WeArt.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # or use ' mysql.connector.django ''
        'NAME': 'weArt',
        'USER': 'root',
        'PASSWORD': 'lidaxiang',
        'HOST':'localhost',
        'PORT':'3306',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

# if USE_TZ is True,the database must store the UTC time
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
# STATIC_URL = '/static/'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# session settings
SESSION_COOKIE_AGE = 60*60*24
SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# SESSION_FILE_PATH = "/home/lidaxiang/WeArtSession"

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'weartRegister@gmail.com'
EMAIL_HOST_PASSWORD = 'weArt2017'  #not email's password ,this is Authentication code.
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DOMAIN = "127.0.0.1:8000"

# This is remote GIT server ip address.And it needs to be changed when changing git-server.
GIT_SERVER_IP = "192.168.122.149"
GIT_SERVER_IP_1 = "192.168.122.171"
GIT_SERVER_USER = "lidaxiang"
GIT_SERVER_USERPASSWD = "lidaxiang"

# script file name
# this file is in doc/scripts and it should be moved to user home directory in git server 
SCRIPT_MKDIR = " mkdir_from_web_server.py"

# the port when user register to become reader
REGISTER_SERVER_DOMAIN = socket.gethostbyname(socket.gethostname()) + ":8000"
