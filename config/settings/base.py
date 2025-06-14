import os
from pathlib import Path
from datetime import timedelta
import pymongo
from urllib.parse import quote_plus

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# MongoDB Connection
MONGODB_URI = os.environ.get('MONGODB_URI')
MONGODB_CLIENT = pymongo.MongoClient(MONGODB_URI)
MONGODB_DB = MONGODB_CLIENT[os.environ.get('MONGODB_NAME')]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'drf_spectacular',
    'drf_spectacular_sidecar',
    
    # Local apps
    'apps.users',
    'apps.drinks',
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

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
}

# Internationalization
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom user model
AUTH_USER_MODEL = 'users.User'

# Drf Spectacular Settings
SPECTACULAR_SETTINGS = {
    'TITLE': 'MixMaster API',
    'DESCRIPTION': '''
API do MixMaster - Sistema de Gerenciamento de Drinks com IA

Esta API fornece endpoints para:
- Gerenciamento de drinks e seus componentes
- Tipos de ingredientes e utensílios
- Unidades de medida
- Perfis de sabor
- Ingredientes e utensílios
- Receitas de drinks
- Autenticação de usuários
- Gerenciamento de usuários
    ''',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': True,
        'defaultModelsExpandDepth': 3,
        'defaultModelExpandDepth': 3,
        'docExpansion': 'list',
        'filter': True,
    },
    'SWAGGER_UI_DIST': 'SIDECAR',
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
    'TAGS': [
        {'name': 'auth', 'description': 'Endpoints de autenticação'},
        {'name': 'users', 'description': 'Gerenciamento de usuários'},
        {'name': 'drinks', 'description': 'Gerenciamento de drinks'},
        {'name': 'ingredients', 'description': 'Gerenciamento de ingredientes'},
        {'name': 'utensils', 'description': 'Gerenciamento de utensílios'},
        {'name': 'reference', 'description': 'Dados de referência (tipos, unidades, etc)'},
    ],
    'ENUM_GENERATE_CHOICE_DESCRIPTION': True,
    'ENUM_NAME_OVERRIDES': {
        'NivelDificuldadeEnum': [
            ('facil', 'Fácil'),
            ('medio', 'Médio'),
            ('dificil', 'Difícil')
        ],
        'TeorAlcoolicoEnum': [
            ('zero', 'Zero'),
            ('baixo', 'Baixo'),
            ('medio', 'Médio'),
            ('alto', 'Alto')
        ],
        'TipoUnidadeEnum': [
            ('volume', 'Volume'),
            ('peso', 'Peso'),
            ('unidade', 'Unidade')
        ]
    }
}