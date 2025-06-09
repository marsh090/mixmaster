import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

User = get_user_model()

def create_superuser():
    email = 'admin@admin.com'
    if not User.objects.filter(email=email).exists():
        User.objects.create_superuser(
            username='admin',
            email=email,
            password='admin123'
        )
        print('Superuser created successfully!')
        print(f'Login with email: {email}')
        print('Password: admin123')
    else:
        print('Superuser already exists.')
        print(f'Login with email: {email}')
        print('Password: admin123')

if __name__ == '__main__':
    create_superuser() 