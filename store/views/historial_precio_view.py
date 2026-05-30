from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from store.models import HistorialPrecio
from store.serializers import HistorialPrecioSerializer
from store.pagination import StandardResultsPagination
from store.permissions import EsAdminOSoloLectura
from store.filters import HistorialPrecioFilter


class HistorialPrecioViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (
        HistorialPrecio.objects
        .select_related('id_producto', 'id_sucursal')
        .all()
    )
    serializer_class = HistorialPrecioSerializer
    pagination_class = StandardResultsPagination
    permission_classes = [EsAdminOSoloLectura]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = HistorialPrecioFilter
    search_fields = ['id_producto__nombre', 'id_producto__marca', 'id_sucursal__nombre_sucursal']
    ordering_fields = ['id_historial', 'precio_registrado', 'fecha_registro']
    ordering = ['-fecha_registro']
