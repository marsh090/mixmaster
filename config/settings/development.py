from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'mixmaster-09dz.onrender.com']

# CORS settings for development
CORS_ALLOW_ALL_ORIGINS = True  # Only for development
CORS_ALLOW_CREDENTIALS = True

# MongoDB settings (connection will be established when needed)
MONGODB_URI = os.environ.get('MONGODB_URI')
MONGODB_NAME = os.environ.get('MONGODB_NAME')