from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
        Cria e salva um usuario com email e senha fornecidos
        """
        if not email:
            raise ValueError('O usuario deve ter um email')
        if not password:
            raise ValueError('Senha não pode ficar em branco')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        """
        Cria e salva um superusuario com email e senha fornecidos
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)
        return self.create_user(email, password, **extra_fields)
    

class User(AbstractUser):
    username = None
    name = models.CharField('Nome', max_length=255)
    email = models.EmailField('Email', unique=True)
    password = models.CharField('Senha', max_length=255)
    is_admin = models.BooleanField('Admin', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.email
    
