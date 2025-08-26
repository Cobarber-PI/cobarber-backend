from rest_framework.serializers import ModelSerializer

from core.models import User
from datetime import date

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        depth = 1


class ClienteSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'cellphone', 'DOB', 'cpf']
        extra_kwargs = {'password': {'write_only': True}}

    # Valida se o email é único
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email já está em uso.")
        return value

    # Valida se o CPF é único
    def validate_cpf(self, value):
        cpf_normalizado = value.replace('.', '').replace('-', '')
        if User.objects.filter(cpf=cpf_normalizado).exists():
            raise serializers.ValidationError("Este CPF já está em uso.")
        return cpf_normalizado

    # Valida idade mínima de 16 anos
    def validate_DOB(self, value):
        hoje = date.today()
        idade = hoje.year - value.year
        if (hoje.month, hoje.day) < (value.month, value.day):
            idade -= 1
        if idade < 16:
            raise serializers.ValidationError("O usuário deve ter pelo menos 16 anos.")
        return value

    # Valida se o celular é único
    def validate_cellphone(self, value):
        celular_normalizado = value.replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
        if User.objects.filter(cellphone=celular_normalizado).exists():
            raise serializers.ValidationError("Este número de celular já está em uso.")
        return celular_normalizado

    # Valida tamanho mínimo da senha
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("A senha deve ter pelo menos 8 caracteres.")
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