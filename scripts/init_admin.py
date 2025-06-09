import os
import sys
import django
from django.contrib.auth import get_user_model

print('Initializing admin user creation script...')

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
        sys.exit(1)

if __name__ == '__main__':
    create_superuser()
    print('Script completed successfully.') 