import os
import sys
from pathlib import Path

# Adiciona o diretório raiz do projeto ao PYTHONPATH
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

import django
from django.contrib.auth import get_user_model

print('Initializing admin user creation script...')
print(f'Project root directory: {BASE_DIR}')
print(f'Python path: {sys.path}')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

print('Django setup completed.')

User = get_user_model()
print(f'Using auth model: {User.__name__}')

def create_superuser():
    print('Starting superuser creation process...')
    email = 'mix@master.com'
    password = 'admin123'
    name = 'admin'
    
    try:
        if User.objects.filter(email=email).exists():
            print(f'User with email {email} already exists.')
            user = User.objects.get(email=email)
            # Update password just in case
            user.set_password(password)
            user.save()
            print('Password updated successfully.')
        else:
            print(f'Creating new superuser with email {email}')
            User.objects.create_superuser(
                email=email,
                password=password,
                name=name
            )
            print('Superuser created successfully!')
        
        print('Current superusers in database:')
        for user in User.objects.filter(is_superuser=True):
            print(f'- Name: {user.name}, Email: {user.email}')
            
    except Exception as e:
        print(f'Error creating superuser: {str(e)}')
        print(f'Current directory: {os.getcwd()}')
        print(f'Directory contents: {os.listdir()}')
        sys.exit(1)

if __name__ == '__main__':
    create_superuser()
    print('Script completed successfully.') 