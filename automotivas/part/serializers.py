from rest_framework import serializers
from .models import Part

class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = ['id', 'part_number', 'name', 'details', 'price', 'quantity', 'updated_at']

