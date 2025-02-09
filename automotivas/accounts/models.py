import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

class User(AbstractUser):
    """
    Modelo para Usuario
    """

    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )

    USER_TYPE_CHOICES = (
        ('common', 'Usuário Comum'),
        ('admin', 'Administrador'),
    )

    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='common',
        help_text="Define se o usuário é comum ou administrador."
    )

    @property
    def token(self):
        """
        Retorna um token JWT (access token) para o usuário.
        """
        refresh = RefreshToken.for_user(self)
        return str(refresh.access_token)

    def __str__(self):
        return self.username
