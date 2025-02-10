from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Part
from .serializers import PartSerializer
from car.models import Car


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permite que apenas usuários administradores possam realizar operações de escrita.
    Usuários autenticados podem realizar operações de leitura (GET, HEAD, OPTIONS).
    """
    def has_permission(self, request, view):
        # Permite acesso a métodos seguros se o usuário estiver autenticado
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        # Para métodos não seguros (POST, PUT, PATCH, DELETE), exige que o usuário seja admin
        return request.user and request.user.is_authenticated and request.user.user_type == 'admin'

class PartViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar as Part (peças).
    
    - Usuários comuns (user_type: common): podem apenas listar e visualizar detalhes.
    - Administradores (user_type: admin): podem criar, atualizar e remover peças.
    """
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    permission_classes = [IsAdminOrReadOnly]

    @action(detail=True, methods=['post'], permission_classes=[IsAdminOrReadOnly])
    def associate_carmodels(self, request, pk=None):
        """
        Associa uma ou mais peças a modelos de carro.
        Espera um JSON com 'car_model_ids' (lista de IDs de CarModel).
        """
        part = self.get_object()
        car_model_ids = request.data.get('car_model_ids', [])
        if not isinstance(car_model_ids, list):
            return Response({"detail": "car_model_ids deve ser uma lista."}, status=status.HTTP_400_BAD_REQUEST)
        
        car_models = CarModel.objects.filter(id__in=car_model_ids)
        if not car_models.exists():
            return Response({"detail": "Nenhum CarModel encontrado com os IDs fornecidos."}, status=status.HTTP_400_BAD_REQUEST)
        
        part.car_models.add(*car_models)
        part.save()
        serializer = self.get_serializer(part)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminOrReadOnly])
    def disassociate_carmodel(self, request, pk=None):
        """
        Desassocia um modelo de carro de uma peça.
        Espera um JSON com 'car_model_id'.
        """
        part = self.get_object()
        car_model_id = request.data.get('car_model_id', None)
        if not car_model_id:
            return Response({"detail": "car_model_id é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            car_model = CarModel.objects.get(id=car_model_id)
            part.car_models.remove(car_model)
            part.save()
            serializer = self.get_serializer(part)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CarModel.DoesNotExist:
            return Response({"detail": "CarModel não encontrado."}, status=status.HTTP_404_NOT_FOUND)

