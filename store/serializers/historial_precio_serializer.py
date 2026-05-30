from rest_framework import serializers
from store.models import HistorialPrecio


class HistorialPrecioSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialPrecio
        fields = '__all__'
        read_only_fields = fields
