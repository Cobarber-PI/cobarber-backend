from rest_framework.viewsets import ModelViewSet
from core.models import Barbearia, Comodidades, servicos_oferecidos, Horario_de_funcionamento
from core.serializers.Barbearia import BarbeariaSerializer, ComodidadesSerializer, servicos_oferecidosSerializer,Horario_de_funcionamentoSerializer



class BarbeariaViewSet(ModelViewSet):
    queryset = Barbearia.objects.all().order_by('id')
    serializer_class = BarbeariaSerializer


class ComodidadesViewSet(ModelViewSet):
    queryset = Comodidades.objects.all().order_by('id')
    serializer_class = ComodidadesSerializer


class servicos_oferecidosViewSet(ModelViewSet):
    queryset = servicos_oferecidos.objects.all().order_by('id')
    serializer_class = servicos_oferecidosSerializer

class Horario_de_funcionamentoViewSet(ModelViewSet):
    queryset = Horario_de_funcionamento.objects.all().order_by('id')
    serializer_class = Horario_de_funcionamentoSerializer

