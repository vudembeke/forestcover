from rest_framework import serializers
from .models import ForestData

class ForestDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForestData
        fields = ['ndvi', 'area', 'density', 'change', 'year']

class ForestSerializer(serializers.Serializer):
    forest_name = serializers.CharField(max_length=255)
    data = ForestDataSerializer(many=True)
