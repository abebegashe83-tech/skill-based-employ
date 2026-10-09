import os

from django.core.exceptions import ImproperlyConfigured

from .base import *

if not os.environ.get('SECRET_KEY') or SECRET_KEY in {
    'dev-secret-key',
    'replace-with-a-long-random-development-secret',
    'replace-this-with-a-very-secret-production-key',
}:
    raise ImproperlyConfigured('Set a unique SECRET_KEY in the production environment.')

if not os.environ.get('DATABASE_URL'):
    raise ImproperlyConfigured('Set DATABASE_URL to a persistent production database.')

DEBUG = False
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']
if os.environ.get('ALLOWED_HOSTS'):
    ALLOWED_HOSTS.extend(os.environ['ALLOWED_HOSTS'].split(','))
if os.environ.get('RAILWAY_PUBLIC_DOMAIN'):
    ALLOWED_HOSTS.append(os.environ['RAILWAY_PUBLIC_DOMAIN'])
if os.environ.get('RENDER_EXTERNAL_HOSTNAME'):
    ALLOWED_HOSTS.append(os.environ['RENDER_EXTERNAL_HOSTNAME'])

if DATABASES['default']['ENGINE'] != 'django.db.backends.postgresql':
    raise ImproperlyConfigured('Production requires a persistent PostgreSQL DATABASE_URL.')

CORS_ALLOW_ALL_ORIGINS = False
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',')
    if origin.strip()
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 3600
