from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from pymongo import MongoClient
from .models import User

@receiver(post_save, sender=User)
def sync_user_to_mongodb(sender, instance, created, **kwargs):
    """
    Signal para sincronizar usuários do Django com MongoDB
    """
    client = MongoClient(settings.MONGODB_URI)
    db = client[settings.MONGODB_NAME]
    users_collection = db['users']

    # Preparar dados do usuário para MongoDB
    user_data = {
        'email': instance.email,
        'name': instance.name,
        'is_active': instance.is_active,
        'is_staff': instance.is_staff,
        'is_superuser': instance.is_superuser,
        'is_admin': instance.is_admin,
        'date_joined': instance.date_joined.isoformat(),
        'last_login': instance.last_login.isoformat() if instance.last_login else None,
        '_id': str(instance.id)  # Usar o ID do Django como _id no MongoDB
    }

    # Atualizar ou inserir no MongoDB
    users_collection.update_one(
        {'_id': str(instance.id)},
        {'$set': user_data},
        upsert=True
    )

    client.close() 