import uuid
import hashlib
import random
from django.db import models
from car.models import Car


class Part(models.Model):
    """
    Modelo para Part
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    part_number = models.CharField(
        max_length=20,
        unique=True,
        blank=False,
        null=False,
        help_text="Codigo da peça."
    )

    name = models.CharField(
        max_length=30,
        blank=False,
        null=False,
        help_text="Nome da peça."
    )

    details = models.TextField(
        blank=True,
        null=True,
        help_text="Detalhes ou descrição da peça."
    )
    
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Preço da peça."
    )

    quantity = models.IntegerField(
        default=1,
        help_text="Quantidade disponível em estoque."
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Data e hora da última atualização."
    )

    car_models = models.ManyToManyField(
        Car,
        blank=True,
        related_name='parts',
        help_text="Modelos de carro associados à peça."
    )
    
    def __str__(self):
        return f"{self.part_number} - {self.name}"

