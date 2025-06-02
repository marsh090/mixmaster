from django.core.management.base import BaseCommand
from django.conf import settings
from apps.users.models import User

class Command(BaseCommand):
    help = 'Cria um superuser se não existir'

    def handle(self, *args, **kwargs):
        try:
            # Verifica se já existe um superuser
            if not User.objects.filter(email='admin@mixmaster.com').exists():
                # Cria o superuser
                User.objects.create_superuser(
                    email='admin@mixmaster.com',
                    password='admin123',
                    nome='Admin',
                    sobrenome='MixMaster'
                )
                self.stdout.write(self.style.SUCCESS('Superuser criado com sucesso!'))
            else:
                self.stdout.write(self.style.SUCCESS('Superuser já existe.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao criar superuser: {str(e)}')) 