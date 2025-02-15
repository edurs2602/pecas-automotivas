import csv
import io
from celery import shared_task
from .models import Part

@shared_task
def process_csv_file(csv_content):
    """
    Processa o conteúdo de um arquivo CSV para adicionar ou atualizar peças.
    Espera que o CSV possua as colunas: part_number, name, details, price, quantity.
    """
    try:
        # Cria um objeto StringIO a partir do conteúdo recebido
        csv_file = io.StringIO(csv_content)
        reader = csv.DictReader(csv_file)
        for row in reader:
            part_number = row.get('part_number')
            name = row.get('name')
            details = row.get('details')
            price = row.get('price')
            quantity = row.get('quantity')

            try:
                price = float(price)
            except (TypeError, ValueError):
                price = 0.0

            try:
                quantity = int(quantity)
            except (TypeError, ValueError):
                quantity = 0

            Part.objects.update_or_create(
                part_number=part_number,
                defaults={
                    'name': name,
                    'details': details,
                    'price': price,
                    'quantity': quantity,
                }
            )
    except Exception as e:
        print(f"Erro ao processar o arquivo CSV: {e}")

