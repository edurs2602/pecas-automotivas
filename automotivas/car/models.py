import uuid
from django.db import models


class Car(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    name = models.CharField(
        max_length=15,
        blank=False,
        null=False,
        help_text="Nome do carro."
    )

    manufacturer = models.CharField(
        max_length=20,
        blank=False,
        null=False,
        help_text="Nome do fabricante."
    )

    year = models.IntegerField(
        default=0,
        help_text="Ano do veiculo.",
        blank=False,
        null=False
    )

    def __str__(self):
        return f"{self.name} ({self.year}) - {self.manufacturer}"

