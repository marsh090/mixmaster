from .base import *

DEBUG = False
ALLOWED_HOSTS = ['.vercel.app']  # Adicione seu domínio aqui

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
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True