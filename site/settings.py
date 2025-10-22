"""Django settings for the Ventreo project."""
from __future__ import annotations

from datetime import timedelta
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent

# Initialise environment configuration with sensible defaults.
env = environ.Env(
    DEBUG=(bool, True),
    SECRET_KEY=(str, 'django-insecure-++8lo8)et%)99mze__@qb+)i(v)exn7sue#j6oxh&%=gsif&zf'),
    ALLOWED_HOSTS=(list, []),
    STATIC_ROOT=(str, str(BASE_DIR / 'staticfiles')),
    APP_LOG_DIR=(str, str(BASE_DIR / 'log')),
    AUTH_JWT_ACCESS_LIFETIME_HOURS=(int, 1),
    AUTH_JWT_REFRESH_LIFETIME_DAYS=(int, 1),
    AUTH_JWT_ROTATE_REFRESH_TOKENS=(bool, True),
    AUTH_JWT_ALGORITHM=(str, 'HS256'),
    AUTH_API_RATE_LIMIT_ANONYMOUS=(str, '100/hour'),
    AUTH_API_RATE_LIMIT_AUTHENTICATED=(str, '1000/hour'),
    AUTH_LOGIN_RATE_LIMIT=(str, '5/minute'),
    AUTH_PASSWORD_RESET_RATE_LIMIT=(str, '3/hour'),
    CORS_ALLOWED_ORIGINS=(list, []),
)

# Load optional .env file when present.
env_path = BASE_DIR / '.env'
if env_path.exists():
    environ.Env.read_env(str(env_path))

DEBUG = env('DEBUG')
SECRET_KEY = env('SECRET_KEY')
ALLOWED_HOSTS: list[str] = env('ALLOWED_HOSTS')
ALLOWED_HOSTS.extend(['testserver', 'localhost', '127.0.0.1'])
ALLOWED_HOSTS = list(dict.fromkeys(ALLOWED_HOSTS))

STATIC_URL = 'static/'
STATIC_ROOT = Path(env('STATIC_ROOT'))

# Ensure logging directories exist before Django configures log handlers.
app_log_dir = Path(env('APP_LOG_DIR'))
app_log_dir.mkdir(parents=True, exist_ok=True)
callcenter_log_dir = app_log_dir / 'callcenter'
callcenter_log_dir.mkdir(parents=True, exist_ok=True)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'drf_spectacular',
    'corsheaders',
    'django_extensions',
    'django_user_agents',
    'django_ratelimit',
    # Local apps
    'authentication',
    'modules.identity',
    'modules.access_control',
    'modules.audit',
    'modules.finance',
    'modules.dashboards',
    'modules.notifications',
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
    'django_user_agents.middleware.UserAgentMiddleware',
]

ROOT_URLCONF = 'site.urls'

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

WSGI_APPLICATION = 'site.wsgi.application'
ASGI_APPLICATION = 'site.asgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOWED_ORIGINS = env('CORS_ALLOWED_ORIGINS')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'authentication.permissions.CallCenterPermission',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': env('AUTH_API_RATE_LIMIT_ANONYMOUS'),
        'user': env('AUTH_API_RATE_LIMIT_AUTHENTICATED'),
        'login': env('AUTH_LOGIN_RATE_LIMIT'),
        'password_reset': env('AUTH_PASSWORD_RESET_RATE_LIMIT'),
    },
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# Local caches are sufficient for development and automated testing.
SILENCED_SYSTEM_CHECKS = ['django_ratelimit.E003', 'django_ratelimit.W001']

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=env('AUTH_JWT_ACCESS_LIFETIME_HOURS')),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=env('AUTH_JWT_REFRESH_LIFETIME_DAYS')),
    'ROTATE_REFRESH_TOKENS': env('AUTH_JWT_ROTATE_REFRESH_TOKENS'),
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': env('AUTH_JWT_ALGORITHM'),
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Ventreo API',
    'DESCRIPTION': 'Documentación de referencia para la API del proyecto Ventreo.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} {name}: {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'auth_file': {
            'class': 'logging.FileHandler',
            'level': 'INFO',
            'filename': str(callcenter_log_dir / 'auth.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'callcenter.auth': {
            'handlers': ['auth_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
