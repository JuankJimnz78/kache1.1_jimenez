import django_filters
from store.models import Producto, Precio, HistorialPrecio


class ProductoFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    marca = django_filters.CharFilter(lookup_expr='icontains')
    codigo_barras = django_filters.CharFilter(lookup_expr='icontains')
    id_categoria = django_filters.NumberFilter(field_name='id_categoria')
    unidad_medida = django_filters.ChoiceFilter(choices=Producto.UNIDAD_CHOICES)

    class Meta:
        model = Producto
        fields = ['nombre', 'marca', 'codigo_barras', 'id_categoria', 'unidad_medida']


class PrecioFilter(django_filters.FilterSet):
    id_producto = django_filters.NumberFilter(field_name='id_producto')
    id_sucursal = django_filters.NumberFilter(field_name='id_sucursal')
    en_oferta = django_filters.BooleanFilter(field_name='en_oferta')
    precio_min = django_filters.NumberFilter(field_name='precio_actual', lookup_expr='gte')
    precio_max = django_filters.NumberFilter(field_name='precio_actual', lookup_expr='lte')
    id_supermercado = django_filters.NumberFilter(field_name='id_sucursal__id_supermercado')

    class Meta:
        model = Precio
        fields = ['id_producto', 'id_sucursal', 'en_oferta']


class HistorialPrecioFilter(django_filters.FilterSet):
    id_producto = django_filters.NumberFilter(field_name='id_producto')
    id_sucursal = django_filters.NumberFilter(field_name='id_sucursal')
    fecha_desde = django_filters.DateTimeFilter(field_name='fecha_registro', lookup_expr='gte')
    fecha_hasta = django_filters.DateTimeFilter(field_name='fecha_registro', lookup_expr='lte')

    class Meta:
        model = HistorialPrecio
        fields = ['id_producto', 'id_sucursal']
