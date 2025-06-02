from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth.hashers import make_password
from datetime import datetime

class Command(BaseCommand):
    help = 'Cria um superuser se não existir'

    def handle(self, *args, **kwargs):
        try:
            # Pega a coleção de usuários
            users = settings.MONGODB_DB['users']
            
            # Verifica se já existe um superuser
            if not users.find_one({'email': 'admin@mixmaster.com'}):
                # Cria o superuser
                user = {
                    'email': 'admin@mixmaster.com',
                    'password': make_password('admin123'),
                    'nome': 'Admin',
                    'sobrenome': 'MixMaster',
                    'is_active': True,
                    'is_staff': True,
                    'is_superuser': True,
                    'date_joined': datetime.now(),
                    'last_login': None
                }
                users.insert_one(user)
                self.stdout.write(self.style.SUCCESS('Superuser criado com sucesso!'))
            else:
                self.stdout.write(self.style.SUCCESS('Superuser já existe.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao criar superuser: {str(e)}')) 