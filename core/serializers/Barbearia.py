from rest_framework import serializers
from core.models import Comodidades, servicos_oferecidos, Horario_de_funcionamento, Barbearia

class BarbeariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barbearia
        fields = '__all__'

class ComodidadesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comodidades
        fields = '__all__'

class servicos_oferecidosSerializer(serializers.ModelSerializer):
    class Meta:
        model = servicos_oferecidos
        fields = '__all__'

class Horario_de_funcionamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horario_de_funcionamento
        fields = '__all__'


