from rest_framework.viewsets import GenericViewSet
from core.models import User
from rest_framework.decorators import action
from rest_framework.response import Response

class VirarPropViewSet(GenericViewSet):
    #logar usuario pelo ID da rota e toralo owner =true
    queryset = User.objects.all()
    http_method_names = ['get']

    @action(detail=True, methods=['get'])
    def virar(self, request, pk=None):
        try:
            user = self.queryset.get(id=pk)
            user.is_owner = True
            user.save()
            return Response({'status': f'usuario {user.id} atualizado para owner'})
        except User.DoesNotExist:
            return Response({'error': 'Usuário não encontrado'}, status=404)