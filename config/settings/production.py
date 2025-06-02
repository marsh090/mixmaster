from .base import *

DEBUG = False
ALLOWED_HOSTS = ['.vercel.app', 'localhost', '127.0.0.1']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.dummy',  # Não usamos ORM do Django
        'NAME': os.environ.get('MONGODB_NAME'),
    }
}

# MongoDB Connection (usando driver nativo)
import pymongo
from urllib.parse import quote_plus

MONGODB_URI = os.environ.get('MONGODB_URI')
MONGODB_CLIENT = pymongo.MongoClient(MONGODB_URI)
MONGODB_DB = MONGODB_CLIENT[os.environ.get('MONGODB_NAME')]

# Security
SECURE_SSL_REDIRECT = False  # Vercel já lida com SSL
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# CORS
CORS_ALLOW_ALL_ORIGINS = True  # Você pode restringir isso para origens específicas
CORS_ALLOW_CREDENTIALS = True

# Middleware específico para Vercel
MIDDLEWARE.insert(0, 'corsheaders.middleware.CorsMiddleware')