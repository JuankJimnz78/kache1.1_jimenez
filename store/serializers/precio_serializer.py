from rest_framework import serializers
from store.models import Precio
from store.serializers.producto_serializer import ProductoSerializer
from store.serializers.sucursal_serializer import SucursalSerializer


class PrecioSerializer(serializers.ModelSerializer):
    producto_detalle = ProductoSerializer(source='id_producto', read_only=True)
    sucursal_detalle = SucursalSerializer(source='id_sucursal', read_only=True)

    class Meta:
        model = Precio
        fields = '__all__'
