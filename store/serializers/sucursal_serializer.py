from rest_framework import serializers
from store.models import Sucursal
from store.serializers.supermercado_serializer import SupermercadoSerializer


class SucursalSerializer(serializers.ModelSerializer):
    supermercado_detalle = SupermercadoSerializer(source='id_supermercado', read_only=True)

    class Meta:
        model = Sucursal
        fields = '__all__'
