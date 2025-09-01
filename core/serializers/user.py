from rest_framework import serializers
from core.models import User
from datetime import date
from django.contrib.auth.models import Group


# 🔹 Serializer para criação (entrada)
class UserWriteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'cpf', 'cellphone', 'DOB']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_DOB(self, value):
        hoje = date.today()
        idade = hoje.year - value.year
        if (hoje.month, hoje.day) < (value.month, value.day):
            idade -= 1

        if self.initial_data.get("role", "client") == "client" and idade < 16:
            raise serializers.ValidationError("O cliente deve ter pelo menos 16 anos.")
        if self.initial_data.get("role", "client") == "owner" and idade < 18:
            raise serializers.ValidationError("O proprietário deve ter pelo menos 18 anos.")

        return value

    def create(self, validated_data):
        password = validated_data.pop('password')

        # Normaliza CPF e celular
        if validated_data.get('cpf'):
            validated_data['cpf'] = validated_data['cpf'].replace('.', '').replace('-', '')
        if validated_data.get('cellphone'):
            validated_data['cellphone'] = validated_data['cellphone'].replace('(', '').replace(')', '').replace('-', '').replace(' ', '')

        # Cria usuário
        user = User(**validated_data)
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.save()

        # Define grupo de acordo com o role
        if user.role == "client":
            grupo, _ = Group.objects.get_or_create(name='compradores')
        else:
            grupo, _ = Group.objects.get_or_create(name='proprietarios')
        user.groups.add(grupo)

        return user


# 🔹 Serializer para leitura (saída)
class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'cellphone', 'DOB']
