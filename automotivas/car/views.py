from rest_framework import viewsets, permissions
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

