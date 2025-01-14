"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import environ
import os
from pathlib import Path

CLIENT_BASE_URL = 'http://127.0.0.1:3000' # API 통신을 하기위한 클라이언트의 BaseUrl을 말합니다. 해당 URL은 소셜 로그인 콜백 url로도 활용됩니다.
SERVER_BASE_URL = 'http://127.0.0.1:3000' # API 통신을 하기위한 서버의 BaseUrl을 말합니다.
# .env 파일을 읽기 위한 객체 생성
env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# env 파일을 읽습니다.
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# env 파일로부터 rest api 키를 가져옵니다.
KAKAO_REST_API_KEY = env('KAKAO_REST_API_KEY')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-sem85_$(7_@pk!(epmf2tpe#d)00t1nm#3^*&$&xnh*ewzc6qe'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# TODO 특정 호스트만 접속 가능하도록 변경
ALLOWED_HOSTS = ['*'] # 모든 호스트 접속이 가능합니다.


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'social_auth',
    'usr',
    'post',
    'celery',
    'django_celery_results',
    'django_celery_beat',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# TODO 특정 호스트만 접속하도록 허용할것
CORS_ORIGIN_ALLOW_ALL = True # 모든 호스트의 접속을 허용합니다.
# CORS_ORIGIN_WHITELIST = () # 특정 호스트의 접속만을 허용합니다.

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# 기본 데이터 베이스를 mysql로 설정합니다.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DB_NAME'), # DB 이름을 설정합니다.
        'USER': env('DB_USER'), # 접근 사용자 이름을 지정합니다.
        'PASSWORD': env('DB_PASSWORD'), # 접근 비밀번호를 지정합니다.
        'HOST': env('DB_HOST'), # mysql 접근 호스트를 의미합니다.
        'PORT': env('DB_PORT'), # 접근 포트 번호를 의미합니다.
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'usr.User' # usr의 User를 기본 auth 모델로 적용

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'social_auth.authentications.CustomAuthentication',
    ),
}



"""
 아래 부분은 셀러리 세팅을 담당합니다.
"""

CELERY_TIMEZONE = 'Asia/Seoul' # 서울로 시간을 설정합니다.
CELERY_TASK_TRACK_STARTED = True # 작업 문제 보고를 위해 사용됩니다. 작업의 시작과 끝을 추적합니다.
CELERY_RESULT_BACKEND = 'django-db' # 장고 설정의 데이터 베이스를 셀러리 결과 DB로 지정합니다.
CELERY_BROKER_URL = env('CELERY_BROKER_URL') # env 파일로 부터 셀러리 url을 불러옵니다.
CELERY_ACCEPT_CONTENT = ['application/json'] # 셀러리가 데이터를 받는 형식
CELERY_RESULT_SERIALIZER = 'json' # 셀러리가 DB 에 결과를 저장하는 방식
CELERY_TASK_SERIALIZER = 'json' # 셀러리가 테스크를 브로커로 보낼 때 어떤 직렬화 방식을 사용할지를 지정
CELERY_BROKER_CONNECTION_RETRY = True
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# 셀러리 스케쥴 시간을 설정합니다.
CELERY_BEAT_SCHEDULE = {
    'check_and_bomb_post': {
        'task': 'post.tasks.check_and_bomb_post',
        'schedule': 60, # 1분 마다 실행됩니다.
        'options': {
            'expires': 10 # 10초내에 실행되지 않으면 만료됩니다.
        }
    }
}