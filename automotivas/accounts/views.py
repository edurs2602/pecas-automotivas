from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from accounts.models import User
from accounts.serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar as operações CRUD do usuário.
    - Permite criação sem autenticação (registro).
    - As demais operações exigem que o usuário esteja autenticado.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

