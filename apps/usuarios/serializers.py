from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'telefono', 'rol', 'tiene_multas_pendientes', 'is_active', 'date_joined']

class RegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'telefono']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        validated_data['rol'] = 'LECTOR'
        return super().create(validated_data)

class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'telefono', 'rol', 'tiene_multas_pendientes']
        read_only_fields = ['id', 'username', 'rol', 'tiene_multas_pendientes']
