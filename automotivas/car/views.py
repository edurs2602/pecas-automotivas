from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from .models import Car
from .serializers import CarSerializer

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permite que apenas usuários administradores (user_type 'admin') possam
    executar métodos de escrita. Usuários autenticados podem apenas ler.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated and request.user.user_type == 'admin'

class CarViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar a entidade Car.

    - Usuários comuns (user_type: common): podem apenas listar e visualizar os detalhes.
    - Administradores (user_type: admin): podem criar, atualizar e remover registros.
    """
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAdminOrReadOnly]

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def parts(self, request, pk=None):
        """
        Retorna as peças associadas a este CarModel.
        """
        car_model = self.get_object()
        parts = car_model.parts.all()  # 'parts' é o related_name definido no campo many-to-many de Part
        serializer = PartSerializer(parts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


