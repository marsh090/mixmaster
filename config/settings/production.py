from .base import *

DEBUG = False
ALLOWED_HOSTS = ['.vercel.app', 'localhost', '127.0.0.1']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': os.environ.get('MONGODB_NAME'),
        'CLIENT': {
            'host': os.environ.get('MONGODB_URI'),
        }
    }
}

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