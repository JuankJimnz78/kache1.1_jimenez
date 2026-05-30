import pytest
from rest_framework import status
from django.urls import reverse

from store.models import Sucursal
from store.tests.factories import SupermercadoFactory, SucursalFactory, ProductoFactory, PrecioFactory
from decimal import Decimal

pytestmark = pytest.mark.django_db


class TestSucursalCRUD:
    def _payload(self, supermercado, nombre='Norte', ciudad='Quito'):
        return {
            'id_supermercado': supermercado.pk,
            'nombre_sucursal': nombre,
            'ciudad': ciudad,
            'direccion': 'Av. Real Audiencia y Nazacota',
            'activo': True,
        }

    def test_list_sucursales(self, authenticated_client):
        SucursalFactory.create_batch(4)
        url = reverse('sucursal-list')
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 4

    def test_create_sucursal(self, authenticated_client):
        sup = SupermercadoFactory()
        url = reverse('sucursal-list')
        response = authenticated_client.post(url, self._payload(sup), format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Sucursal.objects.filter(nombre_sucursal='Norte').exists()

    def test_retrieve_incluye_supermercado_detalle(self, authenticated_client, sucursal):
        url = reverse('sucursal-detail', kwargs={'pk': sucursal.pk})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'supermercado_detalle' in response.data
        assert response.data['supermercado_detalle']['id_supermercado'] == sucursal.id_supermercado.pk

    def test_update_sucursal(self, authenticated_client, sucursal):
        url = reverse('sucursal-detail', kwargs={'pk': sucursal.pk})
        data = {
            'id_supermercado': sucursal.id_supermercado.pk,
            'nombre_sucursal': 'Sur',
            'ciudad': 'Guayaquil',
            'direccion': 'Av. Kennedy',
            'activo': True,
        }
        response = authenticated_client.put(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        sucursal.refresh_from_db()
        assert sucursal.ciudad == 'Guayaquil'

    def test_partial_update_activo(self, authenticated_client, sucursal):
        url = reverse('sucursal-detail', kwargs={'pk': sucursal.pk})
        response = authenticated_client.patch(url, {'activo': False}, format='json')
        assert response.status_code == status.HTTP_200_OK
        sucursal.refresh_from_db()
        assert sucursal.activo is False

    def test_delete_sucursal(self, authenticated_client, sucursal):
        pk = sucursal.pk
        url = reverse('sucursal-detail', kwargs={'pk': pk})
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Sucursal.objects.filter(pk=pk).exists()

    def test_filtro_por_supermercado(self, authenticated_client):
        sup1 = SupermercadoFactory()
        sup2 = SupermercadoFactory()
        SucursalFactory.create_batch(3, id_supermercado=sup1)
        SucursalFactory(id_supermercado=sup2)
        url = reverse('sucursal-list')
        response = authenticated_client.get(url, {'id_supermercado': sup1.pk})
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 3

    def test_filtro_por_ciudad(self, authenticated_client):
        SucursalFactory(ciudad='Quito')
        SucursalFactory(ciudad='Quito')
        SucursalFactory(ciudad='Guayaquil')
        url = reverse('sucursal-list')
        response = authenticated_client.get(url, {'ciudad': 'Quito'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 2


class TestSucursalProductosEnOferta:
    def test_productos_en_oferta(self, authenticated_client):
        sucursal = SucursalFactory()
        prod1 = ProductoFactory()
        prod2 = ProductoFactory()
        prod3 = ProductoFactory()
        PrecioFactory(id_producto=prod1, id_sucursal=sucursal, en_oferta=True, precio_actual=Decimal('5.00'))
        PrecioFactory(id_producto=prod2, id_sucursal=sucursal, en_oferta=True, precio_actual=Decimal('3.00'))
        PrecioFactory(id_producto=prod3, id_sucursal=sucursal, en_oferta=False, precio_actual=Decimal('8.00'))
        url = reverse('sucursal-productos-en-oferta', kwargs={'pk': sucursal.pk})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert all(item['en_oferta'] for item in response.data)

    def test_productos_en_oferta_orden_precio(self, authenticated_client):
        sucursal = SucursalFactory()
        prod1 = ProductoFactory()
        prod2 = ProductoFactory()
        PrecioFactory(id_producto=prod1, id_sucursal=sucursal, en_oferta=True, precio_actual=Decimal('10.00'))
        PrecioFactory(id_producto=prod2, id_sucursal=sucursal, en_oferta=True, precio_actual=Decimal('4.00'))
        url = reverse('sucursal-productos-en-oferta', kwargs={'pk': sucursal.pk})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert Decimal(response.data[0]['precio_actual']) == Decimal('4.00')

    def test_productos_en_oferta_sucursal_sin_ofertas(self, authenticated_client, sucursal):
        url = reverse('sucursal-productos-en-oferta', kwargs={'pk': sucursal.pk})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == []
