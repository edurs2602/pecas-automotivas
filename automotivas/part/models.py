import uuid
import hashlib
import random
from django.db import models

def generate_part_number():
    """
    Gera um hash de 8 caracteres a partir de um número aleatório.
    """
    random_value = random.getrandbits(128)
    hash_str = hashlib.sha256(str(random_value).encode('utf-8')).hexdigest()
    return hash_str[:8]

class Part(models.Model):
    """
    Modelo para Part, onde o campo part_number é um hash de 10 caracteres que
    também serve como um identificador secundário.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    part_number = models.CharField(
        max_length=8,
        unique=True,
        default=generate_part_number,
        blank=False,
        null=False,
        help_text="Hash de 8 caracteres gerado automaticamente como identificador secundário."
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
    
    def __str__(self):
        return f"{self.part_number} - {self.name}"

