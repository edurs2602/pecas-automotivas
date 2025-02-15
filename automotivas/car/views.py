from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Car
from .serializers import CarSerializer
from part.models import Part
from part.serializers import ListPartSerializer

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permite acesso de leitura para qualquer usuário autenticado e 
    operações de escrita apenas para usuários administradores.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated and request.user.user_type == 'admin'

class CarPagination(PageNumberPagination):
    """
    Configuração de paginação para o endpoint de Car.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class CarViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar a entidade Car.
    
    - Permite filtragem por nome, fabricante e ano.
    - Permite busca e ordenação pelos mesmos campos.
    - Pagina os resultados de listagem.
    - Contém um endpoint customizado 'parts' para retornar as peças associadas ao carro.
    """
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = CarPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'manufacturer', 'year']
    search_fields = ['name', 'manufacturer']
    ordering_fields = ['year', 'name']

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def parts(self, request, pk=None):
        """
        Retorna as peças associadas a este carro.
        
        OBS: Ajuste a query conforme a relação real entre Car e Part.
        Por exemplo, se Car estiver relacionado a Part via uma ForeignKey ou ManyToManyField.
        """
        car = self.get_object()
        parts = Part.objects.filter(car=car)
        serializer = PartSerializer(parts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



