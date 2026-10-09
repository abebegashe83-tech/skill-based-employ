import os
from datetime import timedelta
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / '.env')

SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']
if os.environ.get('ALLOWED_HOSTS'):
    ALLOWED_HOSTS.extend(os.environ['ALLOWED_HOSTS'].split(','))
if os.environ.get('RAILWAY_PUBLIC_DOMAIN'):
    ALLOWED_HOSTS.append(os.environ['RAILWAY_PUBLIC_DOMAIN'])
if os.environ.get('RENDER_EXTERNAL_HOSTNAME'):
    ALLOWED_HOSTS.append(os.environ['RENDER_EXTERNAL_HOSTNAME'])

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'apps.users.apps.UsersConfig',
    'apps.jobs.apps.JobsConfig',
    'apps.applications.apps.ApplicationsConfig',
    'apps.ai_matching.apps.AiMatchingConfig',
    'apps.notifications.apps.NotificationsConfig',
    'apps.admin_api',
    'apps.contact',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3'),
        conn_max_age=600,
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'users.User'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=24),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': False,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:3001',
    'http://127.0.0.1:3000',
    'http://127.0.0.1:3001',
    'http://localhost:5173',
    'http://127.0.0.1:5173',
    'http://localhost:3002',
    'http://127.0.0.1:3002',
    'http://localhost:3003',
    'http://127.0.0.1:3003',
    'http://localhost:3004',
    'http://127.0.0.1:3004',
    'http://localhost:3005',
    'http://127.0.0.1:3005',
]

extra_cors = os.environ.get('CORS_ALLOWED_ORIGINS', '')
for origin in extra_cors.split(','):
    origin = origin.strip()
    if origin and origin not in CORS_ALLOWED_ORIGINS:
        CORS_ALLOWED_ORIGINS.append(origin)

for env_key in ['RAILWAY_FRONTEND_URL', 'VERCEL_FRONTEND_URL']:
    value = os.environ.get(env_key, '')
    if value and value not in CORS_ALLOWED_ORIGINS:
        CORS_ALLOWED_ORIGINS.append(value)

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = DEBUG
CORS_ALLOW_HEADERS = ['content-type', 'authorization', 'x-csrftoken']
CORS_ALLOW_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']

EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@skillmatch.com')
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_FAIL_SILENTLY = False

HF_TOKEN = os.environ.get('HF_TOKEN', '')
FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:3000')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
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
            'stream': 'ext://sys.stdout',
        },
    },
    'root': {'handlers': ['console'], 'level': 'INFO'},
    'loggers': {
        'apps': {'handlers': ['console'], 'level': 'INFO', 'propagate': False},
        'django': {'handlers': ['console'], 'level': 'INFO', 'propagate': False},
    },
}

JAZZMIN_SETTINGS = {
    'site_title': 'Admin Dashboard',
    'site_header': 'Skill-Based Employment Admin',
    'site_brand': 'SBEP Admin',
    'welcome_sign': 'Welcome to Admin Dashboard',
    'copyright': 'Skill-Based Employment Platform',
    'topmenu_links': [
        {'name': 'Home', 'url': 'admin:index'},
        {'name': 'View Site', 'url': '/'},
    ],
    'icons': {
        'auth.user': 'fas fa-user',
        'users.profile': 'fas fa-id-card',
        'users.jobseekerprofile': 'fas fa-user-tie',
        'users.employerprofile': 'fas fa-building',
        'jobs.job': 'fas fa-briefcase',
        'applications.application': 'fas fa-file-alt',
        'notifications.notification': 'fas fa-bell',
        'contact.contactmessage': 'fas fa-envelope',
    },
    'show_sidebar': True,
    'navigation_expanded': True,
    'hide_apps': [],
    'order_with_respect_to': ['auth', 'users', 'jobs', 'applications', 'notifications'],
}
