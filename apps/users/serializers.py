from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'password', 'is_admin', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_admin': {'read_only': True},
        }
    
    def create(self, validated_data):
        """
        Cria um novo usuário com senha criptografada
        """
        user = User.objects.create_user(**validated_data)
        return user
    
    def update(self, instance, validated_data):
        """
        Atualiza um usuário, tratando a senha adequadamente
        """
        password = validated_data.pop('password', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        if password:
            instance.set_password(password)
            
        instance.save()
        return instance
        
        