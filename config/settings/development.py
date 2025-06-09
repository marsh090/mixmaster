from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'mixmaster-09dz.onrender.com']

# CORS settings for development
CORS_ALLOW_ALL_ORIGINS = True  # Only for development
CORS_ALLOW_CREDENTIALS = True

# CSRF settings
CSRF_TRUSTED_ORIGINS = [
    'https://mixmaster-09dz.onrender.com',
    'http://localhost:3000',
    'http://127.0.0.1:3000'
]

# MongoDB settings (connection will be established when needed)
MONGODB_URI = os.environ.get('MONGODB_URI')
MONGODB_NAME = os.environ.get('MONGODB_NAME')