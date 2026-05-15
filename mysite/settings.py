import os
from pathlib import Path

# Побудова шляхів (BASE_DIR вказує на корінь проекту)
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: тримайте ключ у секреті!
SECRET_KEY = 'django-insecure-ell9obn&m5g277flwchx1suy8gb-y+@o-k6-f0#8x*8)y5@4tm'

# SECURITY WARNING: вимикайте DEBUG на продакшені!
DEBUG = True

ALLOWED_HOSTS = []

# Додатки
INSTALLED_APPS = [
    'main',
    'core',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'core' / 'templates',
            BASE_DIR / 'core' / 'templates' / 'registration',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.cart_count', 
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'

# База даних
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Валідація паролів
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Локалізація
LANGUAGE_CODE = 'uk'
TIME_ZONE = 'Europe/Kyiv'
USE_I18N = True
USE_TZ = True

# Статичні файли (CSS, JS)
STATIC_URL = 'static/'
# Краще використовувати Path-об'єкти всюди
STATICFILES_DIRS = [BASE_DIR / 'static'] 

# Медіа файли (Зображення товарів)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Налаштування авторизації
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = 'login' # Можна вказувати name з urls.py замість '/login/'
ALLOWED_HOSTS = ['192.168.1.13', '127.0.0.1', 'localhost']