from rest_framework import viewsets, permissions
from .models import Part
from .serializers import PartSerializer

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

