from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from core.models import User
from datetime import date
from django.contrib.auth.models import Group

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'cpf', 'cellphone', 'DOB']
        extra_kwargs = {'password': {'write_only': True}}


    # Valida idade mínima de 16 anos
    def validate_DOB(self, value):
        hoje = date.today()
        idade = hoje.year - value.year
        if (hoje.month, hoje.day) < (value.month, value.day):
            idade -= 1
        if idade < 16:
            raise serializers.ValidationError("O usuário deve ter pelo menos 16 anos.")
        return value    


    # Criação do usuário
    def create(self, validated_data):
        password = validated_data.pop('password')

        # Normaliza CPF e celular antes de salvar
        validated_data['cpf'] = validated_data['cpf'].replace('.', '').replace('-', '')
        validated_data['cellphone'] = validated_data['cellphone'].replace('(', '').replace(')', '').replace('-', '').replace(' ', '')

        # Cria usuário
        user = User(**validated_data)
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.save()

        # Adiciona usuário ao grupo "compradores"
        grupo, created = Group.objects.get_or_create(name='compradores')
        user.groups.add(grupo)

        return user