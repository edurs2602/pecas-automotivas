from rest_framework import serializers
from .models import Part
from car.models import Car


class PartSerializer(serializers.ModelSerializer):
    car_models = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Car.objects.all(),
        required=False
    )

    class Meta:
        model = Part
        fields = ['id', 'part_number', 'name', 'details', 'price', 'quantity', 'updated_at', 'car_models']

