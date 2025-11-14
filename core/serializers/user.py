from rest_framework import serializers
from core.models import User
from datetime import date
from django.contrib.auth.models import Group    


class UserWriteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True, error_messages={
        'min_length': 'A senha deve ter pelo menos 8 caracteres.'
    })
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'confirm_password', 'cpf', 'cellphone', 'DOB', 'is_owner']
        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_password': {'write_only': True}
        }
        
    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError({"confirm_password": "As senhas não coincidem."})
        return data

    def validate_DOB(self, value):
        hoje = date.today()
        idade = hoje.year - value.year
        if (hoje.month, hoje.day) < (value.month, value.day):
            idade -= 1
        if idade < 16:
            raise serializers.ValidationError("O usuário deve ter pelo menos 16 anos.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('confirm_password', None)

        # Normaliza CPF e celular
        if validated_data.get('cpf'):
            validated_data['cpf'] = validated_data['cpf'].replace('.', '').replace('-', '').replace(' ', '')
        if validated_data.get('cellphone'):
            validated_data['cellphone'] = validated_data['cellphone'].replace('(', '').replace(')', '').replace('-', '').replace(' ', '')

        # Cria usuário
        user = User(**validated_data)
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.save()
        return user


# 🔹 Serializer para leitura (saída)
class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'cellphone', 'DOB', 'is_owner']
