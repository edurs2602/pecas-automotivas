from rest_framework import serializers
from .models import Part
from car.models import Car

class ListPartSerializer(serializers.ModelSerializer):
    """
    Serializer para listagem de peças.
    Retorna apenas: part_number, name, details, price e quantity.
    """

    class Meta:
        model = Part
        fields = ['id', 'part_number', 'name', 'details', 'price', 'quantity']

class PartDetailSerializer(serializers.ModelSerializer):
    """
    Serializer detalhado para Part.
    Retorna todas as informações, inclusive updated_at e os modelos associados.
    """
    car_models = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Car.objects.all(),
        required=False
    )

    class Meta:
        model = Part
        fields = ['id', 'part_number', 'name', 'details', 'price', 'quantity', 'updated_at', 'car_models']

