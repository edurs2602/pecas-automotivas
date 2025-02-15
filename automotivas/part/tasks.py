import csv
from celery import shared_task
from django.core.files.storage import default_storage
from .models import Part

@shared_task
def process_csv_file(file_path):
    """
    Processa um arquivo CSV para adicionar ou atualizar peças.
    Espera que o CSV possua as colunas: part_number, name, details, price, quantity.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                part_number = row.get('part_number')
                name = row.get('name')
                details = row.get('details')
                price = row.get('price')
                quantity = row.get('quantity')

                # Conversão de price para float
                try:
                    price = float(price)
                except (TypeError, ValueError):
                    price = 0.0

                # Conversão de quantity para inteiro
                try:
                    quantity = int(quantity)
                except (TypeError, ValueError):
                    quantity = 0

                # Cria ou atualiza a peça com base no part_number
                # Atenção: o modelo Part precisa ter os campos 'details' e 'quantity'
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
        # Registre ou trate o erro conforme necessário
        print(f"Erro ao processar o arquivo CSV: {e}")
    finally:
        # Remove o arquivo após o processamento
        default_storage.delete(file_path)


