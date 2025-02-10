from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Part
from .serializers import ListPartSerializer, PartDetailSerializer
from car.models import Car


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permite operações de leitura para qualquer usuário autenticado.
    Operações de escrita (POST, PUT, PATCH, DELETE) são permitidas apenas para administradores.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated and request.user.user_type == 'admin'

class PartViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar as peças (Part).

    - Para a listagem (action "list"), utiliza ListPartSerializer (retorna dados resumidos).
    - Para as demais ações (retrieve, create, update, destroy), utiliza PartDetailSerializer.
    - Permite filtragem por part_number, name e price.
    - Contém endpoints customizados para associar e desassociar CarModels.
    """
    queryset = Part.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['part_number', 'name', 'price']
    search_fields = ['part_number', 'name']
    ordering_fields = ['price', 'name']

    def get_serializer_class(self):
        if self.action == 'list':
            return ListPartSerializer
        return PartDetailSerializer

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
        
        car_models = Car.objects.filter(id__in=car_model_ids)
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
            car_model = Car.objects.get(id=car_model_id)
            part.car_models.remove(car_model)
            part.save()
            serializer = self.get_serializer(part)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Car.DoesNotExist:
            return Response({"detail": "CarModel não encontrado."}, status=status.HTTP_404_NOT_FOUND)

