import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

User = get_user_model()

def create_superuser():
    if not User.objects.filter(username='zanon').exists():
        User.objects.create_superuser(
            username='zanon',
            email='lucas.guarnier@globalsys.com.br',
            password='admin123'
        )
        print('Superuser created successfully!')
    else:
        print('Superuser already exists.') 