from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from store.models import Sucursal, Precio
from store.serializers import SucursalSerializer, PrecioSerializer
from store.pagination import StandardResultsPagination
from store.permissions import EsAdminOSoloLectura


class SucursalViewSet(viewsets.ModelViewSet):
    queryset = Sucursal.objects.select_related('id_supermercado').all()
    serializer_class = SucursalSerializer
    pagination_class = StandardResultsPagination
    permission_classes = [EsAdminOSoloLectura]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['id_supermercado', 'ciudad', 'activo']
    search_fields = ['nombre_sucursal', 'ciudad', 'direccion']
    ordering_fields = ['id_sucursal', 'nombre_sucursal', 'ciudad', 'activo']
    ordering = ['id_supermercado', 'nombre_sucursal']

    @action(detail=True, methods=['get'], url_path='productos-en-oferta')
    def productos_en_oferta(self, request, pk=None):
        sucursal = self.get_object()
        precios = (
            Precio.objects
            .filter(id_sucursal=sucursal, en_oferta=True)
            .select_related('id_producto', 'id_sucursal', 'id_sucursal__id_supermercado')
            .order_by('precio_actual')
        )
        serializer = PrecioSerializer(precios, many=True, context={'request': request})
        return Response(serializer.data)
