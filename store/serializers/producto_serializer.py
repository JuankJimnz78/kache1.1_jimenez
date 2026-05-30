from rest_framework import serializers
from store.models import Producto
from store.serializers.categoria_serializer import CategoriaSerializer


class ProductoSerializer(serializers.ModelSerializer):
    categoria_detalle = CategoriaSerializer(source='id_categoria', read_only=True)

    class Meta:
        model = Producto
        fields = '__all__'
